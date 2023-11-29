"use client";

import {Montserrat} from "next/font/google";
import Link from "next/link";
import {cn} from "@/lib/utils";
import {Menu} from "@/components/Menu";

const font = Montserrat({
    weight: "600",
    subsets: ["latin"]
})

const Navbar = () => {
    return (
        <nav className="fixed top-0 left-0 right-0 p-4 bg-transparent flex items-center justify-between z-10">
            <Link href="/" className="flex items-center">
                <div className="relative h-8 w-8 mr-4">
                </div>
                <h1 className={cn("text-2xl font-bold text-white", font.className)}>
                    Global Parcels
                </h1>
            </Link>
            <Menu/>
        </nav>
    )
}
export default Navbar