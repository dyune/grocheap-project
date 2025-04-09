import axios from "axios";

type GroceryItem = {
    id: string;
    name: string;
    brand: string;
    price: number;
    weight: string;
    store: string;
    imageUrl: string;
    storeUrl: string;
};

export async function searchGroceries(search: string): Promise<GroceryItem[]> {
    try {
        const response = await axios.get<{ query: string; items: GroceryItem[] }>(
            "http://localhost:8000/search/items/query",
            { params: { query: search } }
        );
        console.log(response.data.items);
        return response.data.items

    } catch (err) {
        console.error("Error fetching grocery items:", err);
        return [];
    }
}
