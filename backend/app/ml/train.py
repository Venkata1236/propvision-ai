import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from lightgbm import LGBMRegressor
from loguru import logger
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import (
    KFold,
    cross_val_predict,
    train_test_split,
)
from xgboost import XGBRegressor

from app.ml.feature_engineering import (
    add_engineered_features,
)
from app.ml.preprocess import (
    build_preprocessor,
    save_preprocessor,
)

RANDOM_STATE = 42


def train_models() -> None:
    """
    Train stacking ensemble valuation pipeline.
    """

    logger.info("Loading training dataset")

    dataset_path = (
        Path("data/train.csv")
    )

    df = pd.read_csv(dataset_path)

    logger.success(
        f"Dataset loaded with shape: {df.shape}"
    )

    # =========================
    # FEATURE ENGINEERING
    # =========================

    df = add_engineered_features(df)

    logger.success(
        "Feature engineering completed"
    )

    # =========================
    # FEATURES / TARGET
    # =========================

    X = df.drop(
        columns=["SalePrice", "Id"],
        errors="ignore",
    )

    y = df["SalePrice"]

    logger.info(
        f"Feature matrix shape: {X.shape}"
    )

    # =========================
    # TRAIN TEST SPLIT
    # =========================

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=RANDOM_STATE,
        )
    )

    logger.info(
        "Train-test split completed"
    )

    # =========================
    # PREPROCESSING
    # =========================

    preprocessor, feature_names = (
        build_preprocessor(X_train)
    )

    logger.info("Fitting preprocessor")

    X_train_processed = (
        preprocessor.fit_transform(X_train)
    )

    X_test_processed = (
        preprocessor.transform(X_test)
    )

    logger.success(
        "Preprocessing completed"
    )

    # =========================
    # XGBOOST MODEL
    # =========================

    logger.info("Training XGBoost model")

    xgb_model = XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    xgb_model.fit(
        X_train_processed,
        y_train,
    )

    logger.success(
        "XGBoost training completed"
    )

    # =========================
    # LIGHTGBM MODEL
    # =========================

    logger.info("Training LightGBM model")

    lgbm_model = LGBMRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=RANDOM_STATE,
    )

    lgbm_model.fit(
        X_train_processed,
        y_train,
    )

    logger.success(
        "LightGBM training completed"
    )

    # =========================
    # STACKING WITH OOF
    # =========================

    logger.info(
        "Generating out-of-fold predictions"
    )

    kf = KFold(
        n_splits=5,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    xgb_oof = cross_val_predict(
        xgb_model,
        X_train_processed,
        y_train,
        cv=kf,
        n_jobs=-1,
    )

    lgbm_oof = cross_val_predict(
        lgbm_model,
        X_train_processed,
        y_train,
        cv=kf,
        n_jobs=-1,
    )

    logger.success(
        "OOF predictions generated"
    )

    # =========================
    # META MODEL
    # =========================

    logger.info(
        "Training Ridge meta learner"
    )

    meta_X_train = np.column_stack(
        [
            xgb_oof,
            lgbm_oof,
        ]
    )

    meta_model = Ridge(alpha=1.0)

    meta_model.fit(
        meta_X_train,
        y_train,
    )

    logger.success(
        "Meta learner training completed"
    )

    # =========================
    # FINAL PREDICTIONS
    # =========================

    logger.info(
        "Generating stacked predictions"
    )

    xgb_test_pred = xgb_model.predict(
        X_test_processed
    )

    lgbm_test_pred = lgbm_model.predict(
        X_test_processed
    )

    meta_X_test = np.column_stack(
        [
            xgb_test_pred,
            lgbm_test_pred,
        ]
    )

    stacked_predictions = (
        meta_model.predict(meta_X_test)
    )

    # =========================
    # REVERSE LOG TRANSFORM
    # =========================

    y_test_actual = np.expm1(y_test)

    stacked_predictions_actual = (
        np.expm1(stacked_predictions)
    )

    xgb_predictions_actual = np.expm1(
        xgb_test_pred
    )

    # =========================
    # EVALUATION
    # =========================

    stacked_mape = (
        mean_absolute_percentage_error(
            y_test_actual,
            stacked_predictions_actual,
        )
    )

    xgb_mape = (
        mean_absolute_percentage_error(
            y_test_actual,
            xgb_predictions_actual,
        )
    )

    logger.success(
        f"Stacked Model MAPE: "
        f"{stacked_mape:.4f}"
    )

    logger.success(
        f"XGBoost MAPE: "
        f"{xgb_mape:.4f}"
    )

    improvement = (
        xgb_mape - stacked_mape
    )

    logger.success(
        f"Stacking Improvement: "
        f"{improvement:.4f}"
    )

    # =========================
    # SAVE ARTIFACTS
    # =========================

    save_dir = Path(
        "backend/saved_models"
    )

    save_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    logger.info("Saving models")

    joblib.dump(
        xgb_model,
        save_dir / "xgb_model.pkl",
    )

    joblib.dump(
        lgbm_model,
        save_dir / "lgbm_model.pkl",
    )

    joblib.dump(
        meta_model,
        save_dir / "meta_model.pkl",
    )

    save_preprocessor(
        preprocessor,
        save_dir / "preprocessor.pkl",
    )

    with open(
        save_dir / "feature_names.json",
        "w",
    ) as f:
        json.dump(feature_names, f)

    logger.success(
        "All models saved successfully"
    )

    logger.success(
        "Training pipeline completed"
    )


if __name__ == "__main__":
    train_models()