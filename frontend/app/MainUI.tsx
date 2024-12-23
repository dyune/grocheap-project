"use client";

import React, { useState } from "react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from "@/components/ui/accordion";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { Card, CardContent, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { FaDatabase, FaSearch } from "react-icons/fa";
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import {ProductImage} from "@/components/ProductImage";

export function MainUI({
                           searchText,
                           setSearchText,
                           handleSearch,
                           handleFetchPrices,
                           initProducts,
                           error,
                       }: any) {
    const [products, setProducts] = useState(initProducts || []);

    function sortProductsByPrice(order: string) {
        const sortedProducts = [...products].sort((a, b) => {
            const priceA = parseFloat(a.price || "0");
            const priceB = parseFloat(b.price || "0");

            return order === "asc" ? priceA - priceB : priceB - priceA;
        });
        setProducts(sortedProducts); // Update the state
    }

    return (
        <>
            <h1 className="text-5xl font-bold mt-8 mb-6 text-center text-amber-600">GroCheap</h1>

            <form onSubmit={handleSearch} className="w-full max-w-lg mx-auto mb-6 rounded-2xl">
                <Input
                    type="text"
                    placeholder="Search for products..."
                    value={searchText}
                    onChange={(e) => setSearchText(e.target.value)}
                    className="mb-4"
                />

                <div className="max-w-screen flex justify-center items-center space-x-3">
                    <Button
                        text="Search"
                        icon={<FaSearch />}
                        type="submit"
                        className="bg-amber-600 hover:bg-amber-700 text-white px-1 py-2 rounded-full flex items-center gap-2 min-w-[100px]"
                    />
                    <Button
                        text="Fetch Prices"
                        icon={<FaDatabase />}
                        onClick={handleFetchPrices}
                        className="bg-amber-600 hover:bg-amber-700 text-white px-1 rounded-full flex items-center gap-2 min-w-[180px]"
                    />
                    <Select onValueChange={(value) => sortProductsByPrice(value)}>
                        <SelectTrigger
                            className="bg-amber-600 hover:bg-amber-700 text-white px-4 py-2 rounded-full flex items-center gap-2 max-w-[100px]"
                        >
                            <SelectValue placeholder="Sort" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectLabel className="text-gray-500">Order</SelectLabel>
                                <SelectItem value="dsc">Most expensive</SelectItem>
                                <SelectItem value="asc">Least expensive</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                </div>
            </form>

            {error && (
                <div className="flex justify-center items-center my-10">
                    <Alert className="w-[300px] border-red-500 border bg-white shadow-md rounded-md">
                        <div className="flex items-center">
                            <AlertTitle className="text-red-500 font-semibold">Uh-oh!</AlertTitle>
                        </div>
                        <AlertDescription className="mt-2 text-sm text-gray-700">{error}</AlertDescription>
                    </Alert>
                </div>
            )}

            <ScrollArea className="max-w-2xl mx-auto">
                <ScrollBar orientation="vertical" />
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {products.length > 0 ? (
                        products.map((product: any) => (
                            <Card key={product.id} className="shadow-lg border rounded-lg flex flex-col justify-center items-center">
                                {/* Image or Placeholder */}
                                <ProductImage src={product.image_url} />
                                {/* Card Content */}
                                <CardContent className="p-4 flex-grow">
                                    <h3 className="text-lg font-semibold text-center">
                                        {`${product.brand || "No Brand"} ${product.name}`}
                                    </h3>
                                    <p className="text-sm text-gray-500 text-center">
                                        {product.size?.toUpperCase() || "N/A"}
                                    </p>
                                </CardContent>

                                {/* Footer Elements */}
                                <div className="p-4 text-center space-y-2">
                                    <a
                                        href={product.link}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="rounded-xl mb-4 mx-4 py-2 min-h-13 min-w-40 text-sm bg-red-300 inline-block flex items-center justify-center hover:bg-red-400 transition-colors"
                                    >
                                        {`${product.store || "Unknown Store"} - ${product.price || "N/A"}$`}
                                    </a>
                                </div>
                            </Card>
                        ))
                    ) : (
                        <div className="text-center text-gray-500 col-span-full">
                            Search for products for them to appear.
                        </div>
                    )}
                </div>
            </ScrollArea>


        </>
    );
}
