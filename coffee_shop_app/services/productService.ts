// This file pulls a list of product data from Firebase, cleans it into a usable array, and gives it to the app to show it in UI screens
import { database } from "@/config/firebase.config";
import { ref, get} from "firebase/database";
import { Product } from "@/types/types";

const productRef = ref(database, 'products');        // Reference to the 'products' node in the Firebase Realtime Database

const fetchProducts = async (): Promise<Product[]> => {
    const snapshot = await get(productRef);     
    const data = snapshot.val();        

    const products: Product[] = [];
    if (data) {
        for (const key in data) {
            if (data.hasOwnProperty(key)){
                products.push({... data[key]});
            }
        }
    }
    return products;
}

export { fetchProducts };