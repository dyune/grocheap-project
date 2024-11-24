"use client";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {Alert, AlertDescription, AlertTitle} from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from "@/components/ui/accordion";
import {ScrollArea, ScrollBar} from "@/components/ui/scroll-area";
import {FaDatabase, FaSearch} from "react-icons/fa";
import {SeparatorHorizontal, Terminal} from "lucide-react";
import {Separator} from "@/components/ui/separator";
import {GiFruitBowl} from "react-icons/gi";
import {AccordiongSubScroller} from "@/components/AccordionSubScroller";

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
                        icon={<FaSearch/>}
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
                            <Terminal className="h-4 w-4 mr-2 text-red-500" />
                            <AlertTitle className="text-red-500 font-semibold">Uh-oh!</AlertTitle>
                        </div>
                        <AlertDescription className="mt-2 text-sm text-gray-700">
                            {error}
                        </AlertDescription>
                    </Alert>
                </div>
            )}

            <Separator className="my-4" orientation="horizontal"></Separator>
            {/* Display Products (Accordion View) */}
            <ScrollArea className="max-w-2xl mx-auto">
                <ScrollBar orientation={"vertical"}></ScrollBar>
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
                                        <div className="flex justify-between items-center w-full px-2">
                                            <span>{`${product.brand} ${product.name}`}</span>
                                            <Badge className="bg-amber-300 text-black ml-2">
                                                {capitalizeFirstLetter(product.category)}
                                            </Badge>
                                        </div>
                                    </AccordionTrigger>
                                    <AccordionContent>
                                        <AccordiongSubScroller data={(product.store_names || []).map((store, index) => ({
                                            id: `${store}-${index}`,
                                            store,
                                            price: product.prices?.[index] || "N/A",
                                        }))} />
                                    </AccordionContent>

                                </AccordionItem>
                            )
                        )
                    ) : undefined}
                </Accordion>
            </ScrollArea>
        </>
    );
}
