import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from "@/components/ui/accordion";
import { Badge } from "@/components/ui/badge";
import capitalizeFirstLetter from "@/components/utils/capitalizeFirstLetter";

interface ProductAccordionProps {
  products: Array<{
    id: number;
    name: string;
    brand: string;
    category: string;
    store_names?: string[];
    prices?: string[];
  }>;
}

export default function ProductAccordion({ products }: ProductAccordionProps) {
  return (
    <Accordion type="single" collapsible className="w-full max-w-lg mx-auto">
      {products.length > 0 ? (
        products.map((product) => (
          <AccordionItem key={product.id} value={`product-${product.id}`}>
            <AccordionTrigger className="text-left">{`${product.brand} ${product.name}`}</AccordionTrigger>
            <AccordionContent className="text-left px-4 py-2 bg-white rounded-md shadow-md border border-amber-300">
              <Badge className="bg-amber-300 text-black mb-2">
                {capitalizeFirstLetter(product.category)}
              </Badge>
              {(product.store_names || []).map((store, index) => (
                <div key={`${store}-${index}`} className="mt-1 text-sm">
                  <span className="text-amber-500">Price at {store}: </span>
                  <span className="text-amber-700">${product.prices?.[index] || "N/A"}</span>
                </div>
              ))}
            </AccordionContent>
          </AccordionItem>
        ))
      ) : (
        <p className="text-center text-foreground mt-4">No products found.</p>
      )}
    </Accordion>
  );
}
