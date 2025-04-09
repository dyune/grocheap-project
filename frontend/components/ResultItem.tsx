import Image from "next/image"
import Link from "next/link"
import { ShoppingCart } from "lucide-react"

type GroceryItem = {
  brand: string
  id: number
  image_url: string
  link: string
  name: string
  price: number
  size: string
  store_id: number
}

export default function ResultItem({ item }: { item: GroceryItem }) {

  const storeMapping: { [key: number]: string } = {
    1: "Super C",
    2: "Maxi",
    3: "IGA",
  };

  return (
    <Link href={item.link} target="_blank" rel="noopener noreferrer">
      <div className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow bg-white">
        <div className="relative w-full h-48">
          <Image
            src={item.image_url || "/placeholder.svg"}
            alt={item.name}
            fill
            style={{ objectFit: "contain" }}
            className="p-4"
          />
        </div>
        <div className="p-4">
          <h2 className="text-lg font-semibold mb-1 text-green-800">{item.name}</h2>
          <p className="text-sm text-gray-600 mb-2">{item.brand}</p>
          <p className="text-sm text-gray-600 mb-2">{item.size}</p>
          <div className="flex justify-between items-center">
            <p className="text-2xl font-bold text-green-600">${item.price.toFixed(2)}</p>
            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
              {storeMapping[item.store_id]}
            </span>
          </div>
          <button className="mt-4 w-full bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 transition-colors flex items-center justify-center">
            <ShoppingCart className="w-5 h-5 mr-2" />
            View Deal
          </button>
        </div>
      </div>
    </Link>
  )
}

