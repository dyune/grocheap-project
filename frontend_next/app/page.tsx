"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from "@/components/ui/accordion";
import { Alert } from "@/components/ui/alert";
import { ScrollArea } from "@/components/ui/scroll-area";

export default function Page() {
  const [searchText, setSearchText] = useState("");
  const [products, setProducts] = useState([]);
  const [error, setError] = useState("");

  const capitalizeFirstLetter = (str: string) => str.charAt(0).toUpperCase() + str.slice(1);

  // Fetch products from the backend
  const fetchProducts = async () => {
    setError(""); // Clear any existing error
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
    setError(""); // Clear any existing error
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
    }
  };

  // Handle Fetch Prices button
  const handleFetchPrices = async () => {
    setError(""); // Clear any existing error
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
    <div className="relative min-h-screen bg-background text-foreground p-8">
      {/* Top-right Fetch Prices Button */}
      <div className="absolute top-4 right-4">
        <Button onClick={handleFetchPrices} className="bg-amber-600 hover:bg-amber-700 text-white">
          Fetch Prices
        </Button>
      </div>

      {/* App Title */}
      <h1 className="text-4xl font-bold mb-6 text-center text-amber-600">GroCheap</h1>

      {/* Search Section */}
      <form onSubmit={handleSearch} className="w-full max-w-md mx-auto mb-6">
        <Input
          type="text"
          placeholder="Search for products..."
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          className="mb-4"
        />
        <Button type="submit" className="w-full bg-amber-600 hover:bg-amber-700 text-white">
          Search
        </Button>
      </form>

      {/* Error Message */}
      {error && (
        <Alert className="mb-6" variant="destructive">
          {error}
        </Alert>
      )}

      {/* Display Products (Accordion View) */}
      <ScrollArea className="max-w-2xl mx-auto">
        <Accordion type="single" collapsible>
          {products.length > 0 ? (
            products.map(
              (product: {
                id: number;
                name: string;
                brand: string;
                category: string;
                store_names?: string[];
                prices?: string[];
              }) => (
                <AccordionItem key={product.id} value={`product-${product.id}`}>
                  <AccordionTrigger>
                    {`${product.brand} ${product.name}`}
                  </AccordionTrigger>
                  <AccordionContent>
                    <Badge className="bg-amber-300 text-black">
                      {capitalizeFirstLetter(product.category)}
                    </Badge>
                    {(product.store_names || []).map((store, index) => (
                      <div key={`${store}-${index}`} className="mt-2">
                        <span className="text-amber-500">Price at {store}: </span>
                        <span className="text-amber-700">${product.prices?.[index] || "N/A"}</span>
                      </div>
                    ))}
                  </AccordionContent>
                </AccordionItem>
              )
            )
          ) : (
            <p className="text-center text-foreground mt-4">No products found.</p>
          )}
        </Accordion>
      </ScrollArea>
    </div>
  );
}
