import ResultsList from "@/components/ResultsList"
import { ShoppingBasket } from "lucide-react"

export default function Home() {
  return (
    <main className="container mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <div className="inline-block p-2 bg-green-100 rounded-full mb-4">
          <ShoppingBasket className="w-12 h-12 text-green-600" />
        </div>
        <h1 className="text-4xl font-bold mb-2 text-green-800">Grocheap</h1>
        <p className="text-xl text-green-600">Find the cheapest groceries in Montreal!</p>
      </div>
      <ResultsList />
    </main>
  )
}

