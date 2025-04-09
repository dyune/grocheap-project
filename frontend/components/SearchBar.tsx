"use client"

import { useState, useEffect, useRef } from "react"
import { Search } from "lucide-react"
import type React from "react"

export default function SearchBar({ onSearch }: { onSearch: (query: string) => void }) {
  const [query, setQuery] = useState("")
  const debounceTimerRef = useRef<NodeJS.Timeout | null>(null)

  // Debounced search implementation
  // useEffect(() => {
  //   if (!query.trim()) {
  //     return; // Don't search if query is empty
  //   }
  //
  //   debounceTimerRef.current = setTimeout(() => {
  //     onSearch(query);
  //   }, 500);
  //
  //   return () => {
  //     clearTimeout(debounceTimerRef.current);
  //   };
  // }, [query, onSearch]);


  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Immediate search on form submit (button click)
    if (query.trim()) {
      onSearch(query)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value)
    // The actual search is now triggered by the useEffect
  }

  return (
      <form onSubmit={handleSubmit} className="mb-8">
        <div className="flex items-center max-w-2xl mx-auto">
          <input
              type="text"
              value={query}
              onChange={handleInputChange}
              placeholder="Search for groceries..."
              className="flex-grow p-3 border-2 border-green-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
          />
          <button
              type="submit"
              className="bg-green-500 text-white p-3 rounded-r-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
          >
            <Search className="w-6 h-6" />
          </button>
        </div>
      </form>
  )
}