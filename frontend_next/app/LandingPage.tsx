"use client";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {FaSearch} from "react-icons/fa";

export function LandingPage({ searchText, setSearchText, handleSearch }: any) {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen -mt-16">
            {/* Title */}
            <h1 className="text-5xl font-bold text-amber-600 mb-2">GroCheap</h1>

            {/* Subtitle */}
            <p className="mb-5 text-center max-w-xs text-gray-700">
                Search up a grocery item and compare it across grocery stores!
            </p>

            {/* Search Form */}
            <form onSubmit={handleSearch} className="w-full max-w-md mx-auto flex flex-col rounded-2xl items-center">
                {/* Input */}
                <Input
                    type="text"
                    placeholder="Type here..."
                    value={searchText}
                    onChange={(e) => setSearchText(e.target.value)}
                    className="mb-4 w-full"
                />

                {/* Button */}
                <Button
                    text="Search"
                    icon={<FaSearch/>}
                    type="submit"
                    className="flex items-center justify-center bg-amber-600 hover:bg-amber-700 text-white rounded-2xl py-3 px-6 gap-2"
                />
            </form>
        </div>


    );
}
