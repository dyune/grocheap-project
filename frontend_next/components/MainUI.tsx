import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Alert } from "@/components/ui/alert";
import ProductAccordion from "@/components/ProductAccordion";

interface MainUIProps {
  products: Array<any>;
  error: string;
  searchText: string;
  setSearchText: (text: string) => void;
  onSearch: (query: string) => void;
  onFetchPrices: () => void;
}

export default function MainUI({
  products,
  error,
  searchText,
  setSearchText,
  onSearch,
  onFetchPrices,
}: MainUIProps) {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchText.trim()) {
      onSearch(searchText);
    }
  };

  return (
    <div className="absolute inset-0 transition-all duration-200 opacity-100 visible translate-y-0">
      <div className="absolute top-4 right-4">
        <Button onClick={onFetchPrices} className="bg-amber-600 hover:bg-amber-700 text-white">
          Fetch Prices
        </Button>
      </div>
      <h1 className="text-4xl font-bold mb-6 text-center text-amber-600">GroCheap</h1>
      <form onSubmit={handleSubmit} className="w-full max-w-md mx-auto mb-6">
        <Input
          type="text"
          placeholder="Search for products..."
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          className="mb-4"
        />
        <Button type="submit" className="w-full bg-amber-600 hover:bg-amber-700 text-white">
          Search
        </Button>
      </form>
      {error && (
        <Alert className="mb-6" variant="destructive">
          {error}
        </Alert>
      )}
      <ProductAccordion products={products} />
    </div>
  );
}
