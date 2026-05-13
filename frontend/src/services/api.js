import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export const valuateProperty = async (
  propertyData
) => {
  const response = await API.post(
    "/valuate",
    propertyData
  );

  return response.data;
};

export default API;