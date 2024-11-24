"use client";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from "@/components/ui/accordion";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { FaDatabase, FaSearch } from "react-icons/fa";
import { Separator } from "@/components/ui/separator";
import { AccordiongSubScroller } from "@/components/AccordionSubScroller";
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card";
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
            <ScrollArea className="max-w-2xl mx-auto">
                <ScrollBar orientation="vertical" />
                <Accordion type="single" collapsible>
                    {products.length > 0 ? (
                        products.map(
                            (product: {
                                id: number;
                                name: string;
                                brand: string;
                                link: string;
                                image_url?: string;
                                size?: string;
                                store?: string;
                                price?: string;
                            }) => (
                                 <AccordionItem key={product.id} value={`product-${product.id}`}>
                                    <AccordionTrigger>
                                        <div className="flex justify-between items-center w-full px-2">
                                            <span>{`${product.brand || "No Brand"} ${product.name}`}</span>
                                        </div>
                                    </AccordionTrigger>
                                    <AccordionContent>
                                        <Card>
                                            <CardTitle><Badge className="text-lg bg-red-300">{`${product.store} ${product.price + "$"}`}</Badge></CardTitle>
                                            <CardContent>
                                            {product.image_url && (
                                                <div>
                                                    <img src={product.image_url} alt={product.name} className="w-32 h-32 object-cover rounded-md" />
                                                </div>
                                            )}
                                                <div className="p-4 space-y-2">
                                                    {/* Product Details */}
                                                    <div>
                                                        <span className="font-bold"></span>
                                                        {product.size?.toUpperCase() || "N/A"}
                                                    </div>
                                                    <div>
                                                            <a href={product.link} className="font-black underline">
                                                                View product
                                                            </a>
                                                    </div>
                                                </div>
                                            </CardContent>
                                        </Card>
                                    </AccordionContent>
                                </AccordionItem>
                            )
                        )
                    ) : (
                        <div className="text-center text-gray-500">No products found.</div>
                    )}
                </Accordion>
            </ScrollArea>
        </>
    );
}
