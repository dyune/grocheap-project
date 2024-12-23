import * as React from "react";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";

export function AccordiongSubScroller({ data }) {
    return (
        <ScrollArea className="w-max whitespace-nowrap rounded-md border bg-white">
            <div className="flex w-max space-x-4 p-4">
                {data.map((elem) => (
                    <div
                        key={elem.id}
                        className="min-w-[200px] bg-gray-100 rounded-lg shadow-md p-4 flex flex-col items-start"
                    >
                        <h4 className="font-semibold text-sm">{elem.store}</h4>
                        <Badge className="mt-2 bg-red-400 text-black">
                            ${elem.price}
                        </Badge>
                    </div>
                ))}
            </div>
            <ScrollBar orientation="horizontal" />
        </ScrollArea>
    );
}
