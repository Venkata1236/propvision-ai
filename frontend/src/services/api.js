import axios from "axios";

const API = axios.create({
  baseURL:
    import.meta.env
      .VITE_API_URL,

  headers: {
    "Content-Type":
      "application/json",
  },
});

export const valuateProperty =
  async (propertyData) => {

    const response =
      await API.post(
        "/valuate",
        propertyData
      );

    return response.data;
  };

export default API;