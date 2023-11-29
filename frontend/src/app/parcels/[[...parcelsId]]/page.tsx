"use client"

import React, {useEffect, useState} from 'react';
import {usePathname, useSearchParams} from 'next/navigation';
import Layout from "@/components/Layout";

interface Parcel {
    id: string;
    name: string;
    parcel_type: string;
    weight: number;
    content_value_cents: number;
    delivery_cost_cents: number;
}

export default function ParcelDetailPage() {
    const pathname = usePathname();
    const searchParams = useSearchParams();
    const [parcel, setParcel] = useState<Parcel | null>(null);
    const [loading, setLoading] = useState<boolean>(true);

    const fetchParcelDetails = async (parcelId: string) => {
        try {
            const response = await fetch(`http://localhost:8000/parcels/${parcelId}`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            setParcel(data);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        const parcelId = pathname.split('/').pop();
        if (parcelId && parcelId !== '[...parcelId]') {
            setLoading(true);
            fetchParcelDetails(parcelId);
        }
    }, [pathname, searchParams]);

    if (loading) {
        return <div style={{color: '#B0BEC5'}}>Loading...</div>;
    }

    if (!parcel) {
        return <div style={{color: '#B0BEC5'}}>Parcel not found.</div>;
    }

    const formattedContentValue = (parcel.content_value_cents / 100).toFixed(2);
    const formattedDeliveryCost = parcel.delivery_cost_cents
        ? (parcel.delivery_cost_cents / 100).toFixed(2)
        : 'N/A';

    return (
        <Layout>
            <div className="p-4" style={{color: '#B0BEC5'}}>
                <h1 className="text-2xl font-bold mb-4">Parcel Details</h1>
                <div className="rounded-md border p-4">
                    <p><strong>ID:</strong> {parcel.id}</p>
                    <p><strong>Name:</strong> {parcel.name}</p>
                    <p><strong>Type:</strong> {parcel.parcel_type}</p>
                    <p><strong>Weight:</strong> {parcel.weight} kg</p>
                    <p><strong>Content Value:</strong> ${formattedContentValue}</p>
                    <p><strong>Delivery Cost:</strong> ${formattedDeliveryCost}</p>
                </div>
            </div>
        </Layout>
    );
}