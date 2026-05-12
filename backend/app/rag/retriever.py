import pickle
from typing import Dict, List

import faiss
import numpy as np
import pandas as pd
from langchain_openai import OpenAIEmbeddings
from loguru import logger

from app.core.config import settings


class ComparableSalesRetriever:
    """
    Retrieve semantically similar property sales using FAISS.
    """

    def __init__(self):
        logger.info(
            "Loading FAISS comparable sales index"
        )

        self.index = faiss.read_index(
            settings.faiss_index_path
        )

        logger.success(
            f"FAISS index loaded with "
            f"{self.index.ntotal} properties"
        )

        logger.info(
            "Loading comparable sales metadata"
        )

        with open(
            settings.faiss_metadata_path,
            "rb",
        ) as f:
            self.metadata = pickle.load(f)

        logger.success(
            "Comparable metadata loaded"
        )

        logger.info(
            "Initializing embedding model"
        )

        self.embedding_model = OpenAIEmbeddings(
            model=settings.openai_embedding_model,
            openai_api_key=settings.openai_api_key,
        )

        logger.success(
            "Retriever initialized successfully"
        )

    def build_query_text(
        self,
        property_data: Dict,
    ) -> str:
        """
        Convert input property into semantic search query.
        """

        return (
            f"Property in "
            f"{property_data.get('Neighborhood', 'Unknown')}. "
            f"Total area: "
            f"{property_data.get('GrLivArea', 0)} sqft. "
            f"Bedrooms: "
            f"{property_data.get('BedroomAbvGr', 0)}. "
            f"Bathrooms: "
            f"{property_data.get('FullBath', 0)}. "
            f"Overall quality: "
            f"{property_data.get('OverallQual', 0)}/10. "
            f"Garage area: "
            f"{property_data.get('GarageArea', 0)} sqft."
        )

    def retrieve_comparable_sales(
        self,
        property_data: Dict,
        top_k: int = 3,
    ) -> List[Dict]:
        """
        Retrieve top similar comparable properties.
        """

        logger.info(
            "Generating comparable sales query"
        )

        query_text = self.build_query_text(
            property_data
        )

        logger.info(
            "Generating query embedding"
        )

        query_embedding = (
            self.embedding_model.embed_query(
                query_text
            )
        )

        query_vector = np.array(
            [query_embedding],
            dtype=np.float32,
        )

        logger.info(
            "Searching FAISS index"
        )

        distances, indices = (
            self.index.search(
                query_vector,
                top_k,
            )
        )

        logger.success(
            f"Retrieved {top_k} comparable sales"
        )

        comparable_results = []

        for idx, distance in zip(
            indices[0],
            distances[0],
        ):

            property_record = (
                self.metadata[idx]
            )

            similarity_score = (
                self._convert_distance_to_similarity(
                    distance
                )
            )

            comparable_results.append(
                {
                    "property_id": int(
                        property_record.get(
                            "Id",
                            0,
                        )
                    ),
                    "description": (
                        self._build_description(
                            property_record
                        )
                    ),
                    "sale_price_inr": int(
                        property_record.get(
                            "SalePrice",
                            0,
                        )
                    ),
                    "sale_date": str(
                        property_record.get(
                            "YrSold",
                            "Unknown",
                        )
                    ),
                    "similarity_score": float(
                        round(similarity_score, 2)
                    ),
                    "neighborhood": (
                        property_record.get(
                            "Neighborhood",
                            "Unknown",
                        )
                    ),
                }
            )

        logger.success(
            "Comparable sales formatting completed"
        )

        return comparable_results

    def _build_description(
        self,
        property_record: Dict,
    ) -> str:
        """
        Generate readable comparable property description.
        """

        bedrooms = property_record.get(
            "BedroomAbvGr",
            0,
        )

        sqft = property_record.get(
            "GrLivArea",
            0,
        )

        neighborhood = (
            property_record.get(
                "Neighborhood",
                "Unknown",
            )
        )

        return (
            f"{bedrooms}BHK, "
            f"{sqft} sqft, "
            f"{neighborhood}"
        )

    def _convert_distance_to_similarity(
        self,
        distance: float,
    ) -> float:
        """
        Convert FAISS L2 distance into similarity score.
        """

        similarity = 1 / (
            1 + distance
        )

        return similarity


if __name__ == "__main__":

    retriever = (
        ComparableSalesRetriever()
    )

    sample_property = {
        "Neighborhood": "NoRidge",
        "GrLivArea": 2400,
        "BedroomAbvGr": 4,
        "FullBath": 3,
        "OverallQual": 8,
        "GarageArea": 500,
    }

    results = (
        retriever.retrieve_comparable_sales(
            sample_property
        )
    )

    logger.success(
        f"Retrieved comparables: {results}"
    )