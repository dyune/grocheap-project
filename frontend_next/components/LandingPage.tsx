import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface LandingPageProps {
  searchText: string;
  setSearchText: (text: string) => void;
  onSearch: (query: string) => void;
}

export default function LandingPage({ searchText, setSearchText, onSearch }: LandingPageProps) {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchText.trim()) {
      onSearch(searchText);
    }
  };

  return (
    <div className="absolute inset-0 flex flex-col items-center justify-center transition-all duration-200 opacity-100 visible translate-y-0">
      <h1 className="text-5xl font-bold mb-6 text-amber-600">GroCheap</h1>
      <form onSubmit={handleSubmit} className="w-full max-w-md mx-auto">
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
    </div>
  );
}
