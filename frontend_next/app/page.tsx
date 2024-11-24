"use client";

import { useState, useEffect } from "react";
import LandingPage from "@/components/LandingPage";
import MainUI from "@/components/MainUI";

export default function Page() {
  const [searchText, setSearchText] = useState("");
  const [products, setProducts] = useState([]);
  const [error, setError] = useState("");
  const [hasSearched, setHasSearched] = useState(false);
  const [isAnimating, setIsAnimating] = useState(false);

  // Fetch all products from the backend
  const fetchProducts = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/items/");
      if (response.ok) {
        const data = await response.json();
        setProducts(data);
      } else {
        setError("Failed to fetch products from the backend.");
      }
    } catch (err) {
      setError("Error connecting to the server.");
      console.error(err);
    }
  };

  // Fetch prices and refresh the product list
  const handleFetchPrices = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/fetch-prices/", { method: "POST" });
      if (response.ok) {
        alert("Prices fetched and updated successfully!");
        fetchProducts();
      } else {
        setError("Failed to fetch prices.");
      }
    } catch (err) {
      setError("Failed to connect to the server.");
      console.error(err);
    }
  };

  // Handle search
  const handleSearch = async (query: string) => {
    setIsAnimating(true);
    setTimeout(() => {
      setHasSearched(true);
      setIsAnimating(false);
    }, 200);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/items/search/?query=${encodeURIComponent(query)}`,
        { method: "GET", headers: { "Content-Type": "application/json" } }
      );

      if (response.status === 200) {
        const data = await response.json();
        setProducts(data);
      } else if (response.status === 404) {
        setError("No items found.");
        setProducts([]);
      } else {
        setError("Failed to search for items.");
      }
    } catch (err) {
      setError("Failed to connect to the server.");
      console.error(err);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  return (
    <div className="relative min-h-screen bg-background text-foreground p-8">
      {!hasSearched && !isAnimating ? (
        <LandingPage
          onSearch={handleSearch}
          searchText={searchText}
          setSearchText={setSearchText}
        />
      ) : (
        <MainUI
          products={products}
          error={error}
          onSearch={handleSearch}
          searchText={searchText}
          setSearchText={setSearchText}
          onFetchPrices={handleFetchPrices}
        />
      )}
    </div>
  );
}
