import json
from pathlib import Path

import joblib
import lightgbm as lgb
import numpy as np
import pandas as pd
import xgboost as xgb
from loguru import logger
from sklearn.linear_model import Ridge
from sklearn.metrics import (
    mean_absolute_percentage_error,
)
from sklearn.model_selection import (
    KFold,
    cross_val_predict,
    train_test_split,
)

from app.ml.preprocess import (
    NUMERICAL_FEATURES,
    CATEGORICAL_FEATURES,
    create_engineered_features,
    create_preprocessor,
    save_preprocessor,
)


RANDOM_STATE = 42


def train_models():

    logger.info(
        "Loading training dataset"
    )

    dataset_path = Path(
        "data/train.csv"
    )

    df = pd.read_csv(dataset_path)

    logger.success(
        f"Dataset loaded: "
        f"{df.shape}"
    )

    # =====================================
    # FEATURE ENGINEERING
    # =====================================

    logger.info(
        "Creating production-safe features"
    )

    # =============================
    # HOUSE AGE
    # =============================

    df["house_age"] = (
        df["YrSold"]
        - df["YearBuilt"]
    )

    # =============================
    # REMODELED FLAG
    # =============================

    df["is_remodeled"] = (
        df["YearBuilt"]
        != df["YearRemodAdd"]
    ).astype(int)

    # =============================
    # GARAGE FLAG
    # =============================

    df["has_garage"] = (
        df["GarageArea"] > 0
    ).astype(int)

    # =============================
    # POOL FLAG
    # =============================

    df["has_pool"] = (
        df["PoolArea"] > 0
    ).astype(int)

    # =============================
    # FLOOR NUMBER MOCK
    # =============================

    df["floor_number"] = 1

    # =============================
    # ENGINEERED FEATURES
    # =============================

    df = create_engineered_features(
        df
    )

    logger.success(
        "Feature engineering completed"
    )

    # =====================================
    # TARGET
    # =====================================

    logger.info(
        "Applying log transform to target"
    )

    y = np.log1p(
        df["SalePrice"]
    )

    # =====================================
    # FEATURE SELECTION
    # =====================================

    selected_features = (
        NUMERICAL_FEATURES
        + CATEGORICAL_FEATURES
    )

    X = df[selected_features]

    logger.success(
        f"Selected features: "
        f"{len(selected_features)}"
    )

    # =====================================
    # TRAIN TEST SPLIT
    # =====================================

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=RANDOM_STATE,
        )
    )

    logger.success(
        "Train-test split completed"
    )

    # =====================================
    # PREPROCESSING
    # =====================================

    logger.info(
        "Fitting preprocessing pipeline"
    )

    preprocessor = (
        create_preprocessor()
    )

    X_train_processed = (
        preprocessor.fit_transform(
            X_train
        )
    )

    X_test_processed = (
        preprocessor.transform(
            X_test
        )
    )

    logger.success(
        "Preprocessing completed"
    )

    # =====================================
    # XGBOOST MODEL
    # =====================================

    logger.info(
        "Training XGBoost model"
    )

    xgb_model = (
        xgb.XGBRegressor(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=5,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=RANDOM_STATE,
        )
    )

    xgb_model.fit(
        X_train_processed,
        y_train,
    )

    logger.success(
        "XGBoost training completed"
    )

    # =====================================
    # LIGHTGBM MODEL
    # =====================================

    logger.info(
        "Training LightGBM model"
    )

    lgbm_model = (
        lgb.LGBMRegressor(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=5,
            random_state=RANDOM_STATE,
        )
    )

    lgbm_model.fit(
        X_train_processed,
        y_train,
    )

    logger.success(
        "LightGBM training completed"
    )

    # =====================================
    # OOF STACKING
    # =====================================

    logger.info(
        "Generating OOF predictions"
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
    )

    lgbm_oof = cross_val_predict(
        lgbm_model,
        X_train_processed,
        y_train,
        cv=kf,
    )

    logger.success(
        "OOF predictions generated"
    )

    # =====================================
    # META LEARNER
    # =====================================

    logger.info(
        "Training Ridge meta learner"
    )

    meta_X_train = np.column_stack(
        [
            xgb_oof,
            lgbm_oof,
        ]
    )

    meta_model = Ridge(
        alpha=1.0
    )

    meta_model.fit(
        meta_X_train,
        y_train,
    )

    logger.success(
        "Meta learner trained"
    )

    # =====================================
    # FINAL PREDICTIONS
    # =====================================

    logger.info(
        "Generating stacked predictions"
    )

    xgb_test_pred = (
        xgb_model.predict(
            X_test_processed
        )
    )

    lgbm_test_pred = (
        lgbm_model.predict(
            X_test_processed
        )
    )

    meta_X_test = np.column_stack(
        [
            xgb_test_pred,
            lgbm_test_pred,
        ]
    )

    stacked_pred_log = (
        meta_model.predict(
            meta_X_test
        )
    )

    stacked_pred = np.expm1(
        stacked_pred_log
    )

    y_test_actual = np.expm1(
        y_test
    )

    # =====================================
    # METRICS
    # =====================================

    stacked_mape = (
        mean_absolute_percentage_error(
            y_test_actual,
            stacked_pred,
        )
    )

    xgb_only_pred = np.expm1(
        xgb_test_pred
    )

    xgb_mape = (
        mean_absolute_percentage_error(
            y_test_actual,
            xgb_only_pred,
        )
    )

    logger.success(
        f"Stacked MAPE: "
        f"{stacked_mape:.4f}"
    )

    logger.success(
        f"XGBoost MAPE: "
        f"{xgb_mape:.4f}"
    )

    logger.success(
        f"Stacking Improvement: "
        f"{xgb_mape - stacked_mape:.4f}"
    )

    # =====================================
    # SAVE ARTIFACTS
    # =====================================

    logger.info(
        "Saving trained artifacts"
    )

    save_dir = Path(
        "saved_models"
    )

    save_dir.mkdir(
        exist_ok=True
    )

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
        save_dir
        / "preprocessor.pkl",
    )

    feature_names = {
        "numerical": (
            NUMERICAL_FEATURES
        ),
        "categorical": (
            CATEGORICAL_FEATURES
        ),
    }

    with open(
        save_dir
        / "feature_names.json",
        "w",
    ) as f:
        json.dump(
            feature_names,
            f,
            indent=4,
        )

    logger.success(
        "All artifacts saved successfully"
    )

    logger.success(
        "Training pipeline completed"
    )


if __name__ == "__main__":

    train_models()