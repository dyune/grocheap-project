"use client";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { FaDatabase, FaSearch } from "react-icons/fa";
import { Separator } from "@/components/ui/separator";
import {Card, CardContent} from "@/components/ui/card";
import React from "react";

export function MainUI({
                           searchText,
                           setSearchText,
                           handleSearch,
                           handleFetchPrices,
                           products,
                           error,
                       }: any) {
    const capitalizeFirstLetter = (str: string) => str.charAt(0).toUpperCase() + str.slice(1);

    return (
        <>
            {/* App Title */}
            <h1 className="text-5xl font-bold mt-8 mb-6 text-center text-amber-600">GroCheap</h1>

            {/* Search Section */}
            <form onSubmit={handleSearch} className="w-full max-w-md mx-auto mb-6 rounded-2xl">
                <Input
                    type="text"
                    placeholder="Search for products..."
                    value={searchText}
                    onChange={(e) => setSearchText(e.target.value)}
                    className="mb-4"
                />

                {/* Buttons Section */}
                <div className="flex justify-center space-x-4">
                    <Button
                        text="Search"
                        icon={<FaSearch />}
                        type="submit"
                        className="bg-amber-600 hover:bg-amber-700 text-white px-6 py-3 rounded-2xl flex items-center gap-2"
                    />
                    <Button
                        text="Fetch Latest Prices"
                        icon={<FaDatabase />}
                        onClick={handleFetchPrices}
                        className="bg-amber-600 hover:bg-amber-700 text-white px-6 py-3 rounded-2xl flex items-center gap-2"
                    />
                </div>
            </form>

            {/* Error Message */}
            {error && (
                <div className="flex justify-center items-center">
                    <Alert className="w-[300px] border-red-500 border bg-white shadow-md rounded-md">
                        <div className="flex items-center">
                            <AlertTitle className="text-red-500 font-semibold">Uh-oh!</AlertTitle>
                        </div>
                        <AlertDescription className="mt-2 text-sm text-gray-700">{error}</AlertDescription>
                    </Alert>
                </div>
            )}

            <Separator className="my-4" orientation="horizontal" />

            {/* Display Products (Accordion View) */}
<ScrollArea className="max-w-7xl mx-auto">
  <ScrollBar orientation="vertical" />
  <div
    className="grid gap-4"
    style={{
      gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
    }}
  >
    {products.length > 0 ? (
      products.map(
        (product: {
          id: number;
          name: string;
          brand: string | null | undefined;
          link: string;
          image_url?: string;
          size?: string;
          store?: string | null | undefined;
          price?: string;
        }) => (
          <Card key={product.id} className="border border-gray-200 shadow-sm rounded-lg flex flex-col">
            {/* Product Image */}
            {product.image_url && (
              <img
                src={product.image_url}
                alt={product.name}
                className="w-full h-40 object-cover rounded-t-lg"
              />
            )}
            <CardContent className="p-4 flex flex-col space-y-2">
              {/* Product Name */}
              <div className="font-bold text-lg text-center">{product.name}</div>

              {/* Price and Store (Badges) */}
              <div className="flex justify-center space-x-2">
                <Badge className="text-xs bg-pink-300">{product.price ? `${product.price}$` : "N/A"}</Badge>
                <Badge className="text-xs bg-red-300">{product.store?.trim() || "Unknown Store"}</Badge>
              </div>

              {/* Product Details */}
              <div className="mt-2 text-sm text-center space-y-1">
                <div>
                  <span className="font-semibold">Size: </span>
                  {product.size?.toUpperCase() || "N/A"}
                </div>
                <div>
                  <a href={product.link} className="text-blue-500 underline">
                    View Product
                  </a>
                </div>
              </div>
            </CardContent>
          </Card>
        )
      )
    ) : (
      <div className="text-center text-gray-500">No products found.</div>
    )}
  </div>
</ScrollArea>

</>
    );
}
