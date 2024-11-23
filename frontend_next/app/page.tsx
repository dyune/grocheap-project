"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import {Badge} from "@/components/ui/badge";
import { ScrollArea } from "@radix-ui/react-scroll-area";

export default function Page() {
  const [searchText, setSearchText] = useState("");
  const [products, setProducts] = useState([]);

  function capitalizeFirstLetter(str: string) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }


  // Fetch products from the backend
  const fetchProducts = async () => {
    try {
      const balls = " balls"
      const response = await fetch(`"http://127.0.0.1:8000/items/${balls}`);
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
        setProducts(data); // Directly set the fetched data
        console.log(data);
      } else if (response.status === 404) {
        alert("No items found.");
        setProducts([]); // Clear the product list
      } else {
        alert("Failed to search for items.");
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
        <Button type="submit" variant="outline">
          Search
        </Button>
      </form>

      {/* Display Products (Scrollable List) */}
      {/* eslint-disable-next-line react/jsx-no-undef */}
      <ScrollArea>
        <div className="max-w-2xl mx-auto mt-6">
          <div className="max-h-96 overflow-y-auto p-4 border border-card-border rounded-lg bg-card">
            {products.length > 0 ? (
                products.map((product: {
                  id: number;
                  name: string;
                  brand: string;
                  category: string;
                  store_names: string[];
                  prices: string[]
                }) => (
                    <Card key={product.id} className="mb-4">
                      <CardHeader>
                        <CardTitle>{product.brand + " " + product.name}</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <Badge>{capitalizeFirstLetter(product.category)}</Badge>
                        {product.store_names.map((store, index) => (
                            <div key={`${store}-${index}`}>
                              Price at {store}: {product.prices[index]}$
                            </div>
                        ))}
                      </CardContent>
                    </Card>
                ))
            ) : (
                <p className="text-center text-foreground">No products found.</p>
            )}
          </div>
        </div>
      </ScrollArea>
    </div>
  );
}
