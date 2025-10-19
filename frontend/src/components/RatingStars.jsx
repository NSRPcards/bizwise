import React, { useState, useEffect } from "react";
import axios from "axios";

export default function RatingStars({ cityName }) {
  const [hover, setHover] = useState(0);
  const [rating, setRating] = useState(0);
  const [average, setAverage] = useState(0);
  const [count, setCount] = useState(0);

  const API_URL = "http://127.0.0.1:8000/ratings"; // backend URL

  // Fetch average rating
  useEffect(() => {
    axios.get(`${API_URL}/${cityName}`)
      .then(res => {
        setAverage(res.data.average_rating);
        setCount(res.data.count);
      })
      .catch(err => console.error(err));
  }, [cityName]);

  const submitRating = (star) => {
    setRating(star);
    axios.post(`${API_URL}/`, {
      user_id: "guest", // replace with real user ID if you have login
      city_name: cityName,
      rating: star
    })
    .then(res => {
      // refresh average rating
      return axios.get(`${API_URL}/${cityName}`);
    })
    .then(res => {
      setAverage(res.data.average_rating);
      setCount(res.data.count);
    })
    .catch(err => console.error(err));
  };

  return (
    <div className="flex items-center space-x-2">
      <div className="flex">
        {[1,2,3,4,5].map((star) => (
          <svg
            key={star}
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill={star <= (hover || rating) ? "gold" : "gray"}
            className="w-5 h-5 cursor-pointer"
            onMouseEnter={() => setHover(star)}
            onMouseLeave={() => setHover(0)}
            onClick={() => submitRating(star)}
          >
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.286 3.96a1 1 0 00.95.69h4.162c.969 0 1.371 1.24.588 1.81l-3.37 2.448a1 1 0 00-.364 1.118l1.287 3.961c.3.922-.755 1.688-1.538 1.118l-3.371-2.448a1 1 0 00-1.175 0l-3.37 2.448c-.783.57-1.838-.196-1.538-1.118l1.286-3.961a1 1 0 00-.364-1.118L2.043 9.387c-.783-.57-.38-1.81.588-1.81h4.162a1 1 0 00.95-.69l1.286-3.96z" />
          </svg>
        ))}
      </div>
      <span className="text-sm text-gray-700">
        {average} ({count})
      </span>
    </div>
  );
}
