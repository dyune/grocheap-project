"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export default function Page() {
  const [searchText, setSearchText] = useState("");
  const [products, setProducts] = useState([]);

  // Fetch products from the backend
  const fetchProducts = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/items/");
      if (response.ok) {
        const data = await response.json();
        setProducts(data);
      } else {
        alert("Failed to fetch products from the backend.");
      }
    } catch (error) {
      alert("An error occurred while fetching products.");
      console.error(error);
    }
  };

  // Handle search submission
  const handleSearch = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!searchText) return;

    try {
      const response = await fetch("http://127.0.0.1:8000/write-text/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: searchText }),
      });

      if (response.ok) {
        alert("Search text saved successfully!");
        setSearchText("");
      } else {
        alert("Failed to save search text.");
      }
    } catch (error) {
      alert("Failed to connect to the server.");
      console.error(error);
    }
  };

  // Handle Fetch Prices button
  const handleFetchPrices = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/fetch-prices/", {
        method: "POST",
      });

      if (response.ok) {
        alert("Prices fetched and updated successfully!");
        fetchProducts(); // Refresh the product list
      } else {
        alert("Failed to fetch prices.");
      }
    } catch (error) {
      alert("Failed to connect to the server.");
      console.error(error);
    }
  };

  // Fetch products on component mount
  useEffect(() => {
    fetchProducts();
  }, []);

  return (
    <div className="relative min-h-screen bg-background text-foreground p-8">
      {/* Top-right Fetch Prices Button */}
      <div className="absolute top-4 right-4">
        <Button onClick={handleFetchPrices} className="bg-button hover:bg-button-hover">
          Fetch Prices
        </Button>
      </div>

      {/* App Title */}
      <h1 className="text-4xl font-bold mb-6 text-center">GroCheap</h1>

      {/* Search Section */}
      <form onSubmit={handleSearch} className="w-full max-w-md mx-auto mb-6">
        <input
          type="text"
          placeholder="Search for products..."
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          className="w-full rounded-md border border-card-border bg-card text-foreground px-4 py-2 mb-4"
        />
        <Button type="submit" className="w-full">
          Search
        </Button>
      </form>

      {/* Display Products (Scrollable List) */}
      <div className="max-w-4xl mx-auto mt-6">
        <div className="max-h-96 overflow-y-auto p-4 border border-card-border rounded-lg bg-card">
          {products.length > 0 ? (
            products.map((product: { id: number; name: string; brand: string; category: string }) => (
              <Card key={product.id} className="mb-4">
                <CardHeader>
                  <CardTitle>{product.name}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p>Brand: {product.brand}</p>
                  <p>Category: {product.category}</p>
                </CardContent>
              </Card>
            ))
          ) : (
            <p className="text-center text-foreground">No products available.</p>
          )}
        </div>
      </div>
    </div>
  );
}
