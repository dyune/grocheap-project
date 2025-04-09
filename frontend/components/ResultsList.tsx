"use client"

import { useState, useEffect } from "react"
import ResultItem from "./ResultItem"
import SearchBar from "./SearchBar"
import { searchGroceries } from "@/lib/api"
import { SlidersHorizontal } from "lucide-react"

type GroceryItem = {
  id: string
  name: string
  brand: string
  price: number
  weight: string
  store: string
  imageUrl: string
  storeUrl: string
}

type SortOption = "price-asc" | "price-desc" | "store" | "most-relevant"

export default function ResultsList() {
  const [results, setResults] = useState<GroceryItem[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [sortOption, setSortOption] = useState<SortOption>("price-asc")
  const [storeFilter, setStoreFilter] = useState<string>("all")

  // Add scrollbar to body on mount to prevent layout shift
  useEffect(() => {
    // Add a class to force scrollbar to always be visible
    document.body.classList.add('force-scrollbar');

    // Clean up when component unmounts
    return () => {
      document.body.classList.remove('force-scrollbar');
    };
  }, []);

  const handleSearch = async (query: string) => {
    setIsLoading(true)
    try {
      const searchResults = await searchGroceries(query)
      setResults(searchResults)
    } catch (error) {
      console.error("Error fetching results:", error)
      // Handle error (e.g., show error message to user)
    } finally {
      setIsLoading(false)
    }
  }

  const stores = Array.from(new Set(results.map((item) => item.store)))

  const sortedAndFilteredResults = results
      .filter((item) => storeFilter === "all" || item.store === storeFilter)
      .sort((a, b) => {
        if (sortOption === "price-asc") return a.price - b.price
        if (sortOption === "price-desc") return b.price - a.price
        if (sortOption === "store") return a.store.localeCompare(b.store)
        return 0
      })

  return (
      <div>
        <SearchBar onSearch={handleSearch} />
        {results.length > 0 && (
            <div className="mb-6 p-4 bg-white rounded-md shadow-md">
              <div className="flex items-center mb-4">
                <SlidersHorizontal className="w-5 h-5 text-green-600 mr-2" />
                <h2 className="text-lg font-semibold text-green-800">Filter & Sort</h2>
              </div>
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div className="w-full sm:w-auto">
                  <label htmlFor="sort" className="block text-sm font-medium text-gray-700 mb-1">
                    Sort by:
                  </label>
                  <select
                      id="sort"
                      value={sortOption}
                      onChange={(e) => setSortOption(e.target.value as SortOption)}
                      className="w-full sm:w-auto p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                  >
                    <option value="most-relevant">Most Relevant</option>
                    <option value="price-asc">Price: Low to High</option>
                    <option value="price-desc">Price: High to Low</option>
                    <option value="store">Store</option>
                  </select>
                </div>
                <div className="w-full sm:w-auto">
                  <label htmlFor="store" className="block text-sm font-medium text-gray-700 mb-1">
                    Filter by store:
                  </label>
                  <select
                      id="store"
                      value={storeFilter}
                      onChange={(e) => setStoreFilter(e.target.value)}
                      className="w-full sm:w-auto p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                  >
                    <option value="all">All Stores</option>
                    {stores.map((store) => (
                        <option key={store} value={store}>
                          {store}
                        </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
        )}
        {isLoading ? (
            <div className="text-center py-8">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-green-500"></div>
              <p className="mt-2 text-green-600">Searching for the best deals...</p>
            </div>
        ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {sortedAndFilteredResults.map((item) => (
                  <ResultItem key={item.id} item={item} />
              ))}
            </div>
        )}
        {results.length === 0 && !isLoading && (
            <div className="text-center py-8">
              <p className="text-gray-600">No results found. Try a different search term.</p>
            </div>
        )}
      </div>
  )
}