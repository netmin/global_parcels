"use client"

import React, {useCallback, useEffect, useState} from 'react';
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable
} from '@tanstack/react-table';
import {Table, TableBody, TableCell, TableHead, TableHeader, TableRow} from '@/components/ui/table';
import {Button} from "@/components/ui/button";
import {Input} from "@/components/ui/input";

import Layout from "@/components/Layout";
import {ChevronLeftIcon, ChevronRightIcon} from "lucide-react";
import {useRouter} from "next/navigation";

type Parcel = {
    id: string;
    name: string;
    weight: number;
    contentValue: number;
    deliveryCost: number | null;
    parcelType: string;
};

const formatCurrency = (amount: number | null) => {
    if (amount == null) return "N/A";
    return new Intl.NumberFormat("ru-RU", {
        style: "currency",
        currency: "RUB",
    }).format(amount / 100);
};

const MyParcelsPage = () => {
    const [data, setData] = useState<Parcel[]>([]);
    const router = useRouter();
    const [sorting, setSorting] = useState([]);
    const [columnFilters, setColumnFilters] = useState([]);
    const [pagination, setPagination] = useState({pageIndex: 0, pageSize: 10});
    const [isLoading, setIsLoading] = useState(false);


    const navigateToParcelDetails = useCallback((parcelId) => {
        router.push(`/parcels/${parcelId}`);
    }, [router]);

    useEffect(() => {
        const fetchData = async () => {
            setIsLoading(true);
            const response = await fetch("http://localhost:8000/parcels/my", {
                method: 'GET',
                credentials: 'include'
            });
            if (response.ok) {
                const newData = await response.json();
                setData(newData);
            } else {
                console.error('Error during data loading');
            }
            setIsLoading(false);
        };

        fetchData();
    }, [pagination.pageIndex, pagination.pageSize]);

    const columns: ColumnDef<Parcel>[] = [
        {accessorKey: 'id', header: 'ID'},
        {accessorKey: 'name', header: 'Name'},
        {accessorKey: 'parcel_type', header: 'Type'},
        {accessorKey: 'weight', header: 'Weight'},
        {
            accessorKey: "content_value_cents",
            header: "Value",
            cell: (info) => formatCurrency(info.getValue())
        },
        {
            accessorKey: "delivery_cost_cents",
            header: "Delivery",
            cell: (info) => formatCurrency(info.getValue())
        }
    ];

    const table = useReactTable({
        data,
        columns,
        state: {
            sorting,
            columnFilters,
            pagination
        },
        onSortingChange: setSorting,
        onColumnFiltersChange: setColumnFilters,
        onPaginationChange: setPagination,
        getCoreRowModel: getCoreRowModel(),
        getSortedRowModel: getSortedRowModel(),
        getFilteredRowModel: getFilteredRowModel(),
        getPaginationRowModel: getPaginationRowModel()
    });

    return (
        <Layout>
            <div className="w-full">
                {isLoading ? (
                    <div>Loading...</div>
                ) : (
                <div className="rounded-md border">
                    <Input
                        value={table.getColumn("name").getFilterValue() ?? ""}
                        onChange={(e) => table.getColumn("name").setFilterValue(e.target.value)}
                        placeholder="Filter by name..."
                    />
                    <Table>
                        <TableHeader>
                            {table.getHeaderGroups().map(headerGroup => (
                                <TableRow key={headerGroup.id}>
                                    {headerGroup.headers.map(header => (
                                        <TableHead key={header.id}>
                                            {flexRender(header.column.columnDef.header, header.getContext())}
                                        </TableHead>
                                    ))}
                                </TableRow>
                            ))}
                        </TableHeader>
                        <TableBody>
                            {table.getRowModel().rows.map(row => (
                                <TableRow key={row.id} className="text-gray-300"
                                          onClick={() => navigateToParcelDetails(row.original.id)}
                                          style={{cursor: 'pointer'}}>
                                    {row.getVisibleCells().map(cell => (
                                        <TableCell key={cell.id}>
                                            {flexRender(cell.column.columnDef.cell, cell.getContext())}
                                        </TableCell>
                                    ))}
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </div> )}
                <div className="flex items-center justify-between px-2 mt-4">
                    <div className="flex items-center space-x-2">
                        <Button
                            variant="outline"
                            className="hidden h-8 w-8 p-0 lg:flex"
                            onClick={() => table.setPageIndex(0)}
                            disabled={!table.getCanPreviousPage()}
                        />
                        <Button
                            variant="outline"
                            className="h-8 w-8 p-0"
                            onClick={() => table.previousPage()}
                            disabled={!table.getCanPreviousPage()}
                        >
                            <ChevronLeftIcon className="h-4 w-4 text-gray-900"/>
                        </Button>
                        <Button
                            variant="outline"
                            className="h-8 w-8 p-0"
                            onClick={() => table.nextPage()}
                            disabled={!table.getCanNextPage()}
                        >
                            <ChevronRightIcon className="h-4 w-4 text-gray-900"/>
                        </Button>
                        <Button
                            variant="outline"
                            className="hidden h-8 w-8 p-0 lg:flex"
                            onClick={() => table.setPageIndex(table.getPageCount() - 1)}
                            disabled={!table.getCanNextPage()}
                        />
                    </div>
                    <div className="flex w-[100px] text-gray-300 items-center justify-center text-sm font-medium">
                        Page {table.getState().pagination.pageIndex + 1} of {table.getPageCount()}
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default MyParcelsPage;