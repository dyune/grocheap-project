export function ProductImage({ src }: { src: string}) {
    const placeholderImage = "https://placehold.co/200x400?text=Image+Unavailable";

    return (
        <img
            src={src}
            onError={(e) => {
                e.currentTarget.onerror = null; // Prevent infinite loop
                e.currentTarget.src = placeholderImage; // Set placeholder image
            }}
            className="w-full h-40 object-cover rounded-t-lg"
        />
    );
}