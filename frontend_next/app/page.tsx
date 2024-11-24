"use client";

import { useState, useEffect } from "react";
import { LandingPage } from "./LandingPage";
import { MainUI } from "./MainUI";
import {
  Menubar,
  MenubarContent,
  MenubarItem,
  MenubarMenu,
  MenubarSeparator,
  MenubarShortcut,
  MenubarTrigger,
} from "@/components/ui/menubar";

export default function Page() {
  const [searchText, setSearchText] = useState("");
  const [products, setProducts] = useState([]);
  const [error, setError] = useState("");
  const [hasSearched, setHasSearched] = useState(false);
  const [loading, setLoading] = useState(false); // Loading state

  // Fetch products from the backend
  const fetchProducts = async () => {
    setError("");
    try {
      const response = await fetch("http://127.0.0.1:8000/items/");
      if (response.ok) {
        const data = await response.json();
        setProducts(data);
      } else {
        setError("Failed to fetch products from the backend.");
      }
    } catch (error) {
      setError("An error occurred while fetching products.");
      console.error(error);
    }
  };

  // Handle search submission
  const handleSearch = async (event: React.FormEvent) => {
    event.preventDefault();
    setError("");
    if (!searchText) return;

    setLoading(true); // Start loading animation
    setHasSearched(true);

    const startTime = Date.now(); // Record the start time

    try {
      const response = await fetch(
          `http://127.0.0.1:8000/items/search/?query=${encodeURIComponent(searchText)}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
          }
      );

      if (response.status === 200) {
        const data = await response.json();
        setSearchText("");
        setProducts(data);
      } else if (response.status === 404) {
        setError("No items found.");
        setProducts([]);
      } else {
        setError("Failed to search for items.");
      }
    } catch (error) {
      setError("Failed to connect to the server.");
      console.error(error);
    } finally {
      const elapsedTime = Date.now() - startTime; // Calculate elapsed time
      const remainingTime = Math.max(0, 1000 - elapsedTime); // Calculate remaining time to reach 1 second

      // Ensure the loading animation lasts for at least 1 second
      setTimeout(() => {
        setLoading(false); // Stop loading animation
      }, remainingTime);
    }
  };

  // Handle Fetch Prices button
  const handleFetchPrices = async () => {
    setError("");
    try {
      const response = await fetch("http://127.0.0.1:8000/fetch-prices/", {
        method: "POST",
      });

      if (response.ok) {
        alert("Prices fetched and updated successfully!");
        fetchProducts(); // Refresh the product list
      } else {
        setError("Failed to fetch prices.");
      }
    } catch (error) {
      setError("Failed to connect to the server.");
      console.error(error);
    }
  };

  // Fetch products on component mount
  useEffect(() => {
    fetchProducts();
  }, []);

  return (
      <>
        <div className="relative min-h-screen bg-background text-foreground p-8">
          {!hasSearched ? (
              <LandingPage
                  searchText={searchText}
                  setSearchText={setSearchText}
                  handleSearch={handleSearch}
              />
          ) : loading ? ( // Display loading animation when loading
              <div className="flex justify-center items-center min-h-screen">
                <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-primary"></div>
              </div>
          ) : (
              <MainUI
                  searchText={searchText}
                  setSearchText={setSearchText}
                  handleSearch={handleSearch}
                  handleFetchPrices={handleFetchPrices}
                  products={products}
                  error={error}
              />
          )}
        </div>
      </>
  );
}
