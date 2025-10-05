const BASE_URL = "http://127.0.0.1:8000/business";

export const getBusinesses = async ({ city, category }) => {
  const query = new URLSearchParams();
  if (city) query.append("location", city);
  if (category) query.append("category", category);

  const response = await fetch(`${BASE_URL}/?${query.toString()}`);
  if (!response.ok) {
    throw new Error("Failed to fetch businesses");
  }
  return response.json();
};
