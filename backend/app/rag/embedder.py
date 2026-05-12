import pickle
from pathlib import Path
from typing import List

import faiss
import numpy as np
import pandas as pd
from langchain_openai import OpenAIEmbeddings
from loguru import logger

from app.core.config import settings


class PropertySalesEmbedder:
    """
    Builds FAISS vector database for comparable sales retrieval.
    """

    def __init__(self):
        logger.info(
            "Initializing OpenAI embedding model"
        )

        self.embedding_model = OpenAIEmbeddings(
            model=settings.openai_embedding_model,
            openai_api_key=settings.openai_api_key,
        )

        logger.success(
            "Embedding model initialized"
        )

    def build_property_text(
        self,
        row: pd.Series,
    ) -> str:
        """
        Convert structured property row into semantic text.
        """

        return (
            f"Property in "
            f"{row.get('Neighborhood', 'Unknown')}. "
            f"Total area: "
            f"{row.get('GrLivArea', 0)} sqft. "
            f"Bedrooms: "
            f"{row.get('BedroomAbvGr', 0)}. "
            f"Bathrooms: "
            f"{row.get('FullBath', 0)}. "
            f"Overall quality: "
            f"{row.get('OverallQual', 0)}/10. "
            f"Garage area: "
            f"{row.get('GarageArea', 0)} sqft. "
            f"Built in "
            f"{row.get('YearBuilt', 0)}. "
            f"Sold price: "
            f"${row.get('SalePrice', 0)}."
        )

    def create_embeddings(
        self,
        texts: List[str],
    ) -> np.ndarray:
        """
        Generate embeddings for property descriptions.
        """

        logger.info(
            f"Generating embeddings for "
            f"{len(texts)} properties"
        )

        embeddings = (
            self.embedding_model.embed_documents(
                texts
            )
        )

        embedding_array = np.array(
            embeddings,
            dtype=np.float32,
        )

        logger.success(
            "Embeddings generated successfully"
        )

        return embedding_array

    def build_faiss_index(
        self,
        df: pd.DataFrame,
    ) -> None:
        """
        Build and persist FAISS vector index.
        """

        logger.info(
            "Building comparable sales index"
        )

        # =========================
        # PROPERTY TEXTS
        # =========================

        property_texts = [
            self.build_property_text(row)
            for _, row in df.iterrows()
        ]

        logger.info(
            "Property descriptions created"
        )

        # =========================
        # EMBEDDINGS
        # =========================

        embeddings = (
            self.create_embeddings(
                property_texts
            )
        )

        # =========================
        # CREATE FAISS INDEX
        # =========================

        embedding_dimension = (
            embeddings.shape[1]
        )

        index = faiss.IndexFlatL2(
            embedding_dimension
        )

        index.add(embeddings)

        logger.success(
            f"FAISS index built with "
            f"{index.ntotal} properties"
        )

        # =========================
        # SAVE INDEX
        # =========================

        faiss_dir = Path(
            "backend/faiss_index"
        )

        faiss_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        faiss.write_index(
            index,
            str(
                faiss_dir
                / "property_index.faiss"
            ),
        )

        logger.success(
            "FAISS index saved successfully"
        )

        # =========================
        # SAVE METADATA
        # =========================

        metadata = df.to_dict(
            orient="records"
        )

        with open(
            faiss_dir / "metadata.pkl",
            "wb",
        ) as f:
            pickle.dump(metadata, f)

        logger.success(
            "Comparable sales metadata saved"
        )


if __name__ == "__main__":

    logger.info(
        "Loading training dataset"
    )

    dataset_path = Path(
        "data/train.csv"
    )

    df = pd.read_csv(dataset_path)

    embedder = (
        PropertySalesEmbedder()
    )

    embedder.build_faiss_index(df)

    logger.success(
        "Comparable sales vector database ready"
    )