"use client"

import {zodResolver} from "@hookform/resolvers/zod";
import {useForm} from "react-hook-form";
import * as z from "zod";

import {Button} from "@/components/ui/button";
import {Select, SelectContent, SelectItem, SelectTrigger, SelectValue} from "@/components/ui/select";
import {Form, FormControl, FormField, FormItem, FormMessage} from "@/components/ui/form";
import {Input} from "@/components/ui/input";

const API_URL = 'http://localhost:8000/parcels';

const parcelTypes = ["clothes", "electronics", "others"];

const formSchema = z.object({
    name: z.string().min(2, {message: "Name must be at least 2 characters."}),
    weight: z.string().transform((val: string) => parseFloat(val)),
    content_value_cents: z.string().transform((val) => parseFloat(val)),
    parcel_type: z.enum(parcelTypes, {message: "Select a valid parcel type."}),
});

const InputField = ({control, name, placeholder, ...rest}) => (
    <FormField
        control={control}
        name={name}
        render={({field}) => (
            <FormItem>
                <FormControl>
                    <Input placeholder={placeholder} {...field} {...rest} />
                </FormControl>
                <FormMessage/>
            </FormItem>
        )}
    />
);

const SelectField = ({control, name, placeholder, options}) => (
    <FormField
        control={control}
        name={name}
        render={({field}) => (
            <FormItem>
                <FormControl>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                        <SelectTrigger>
                            <SelectValue placeholder={placeholder}/>
                        </SelectTrigger>
                        <SelectContent>
                            {options.map(option => (
                                <SelectItem key={option} value={option}>{option}</SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                </FormControl>
                <FormMessage/>
            </FormItem>
        )}
    />
);

export function CreateForm() {
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            name: "",
            weight: "1",
            content_value_cents: "1",
            parcel_type: "",
        },
    });

    const onSubmit = async (values: z.infer<typeof formSchema>) => {
        const payload = {
            ...values,
            session_id: null,
            delivery_cost_cents: null,
            content_value_cents: parseFloat(values.content_value_cents),
            parcel_type_id: null,
        };

        try {
            const resp = await fetch(API_URL, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });
            const data = await resp.json();
            console.log('Success:', data);
            form.reset();
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="p-4 md:p-8 lg:p-12 max-w-screen-sm mx-auto">
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)}
                      className="space-y-6 bg-[#1a2236] p-8 rounded-lg shadow-lg border border-gray-600">

                    <InputField control={form.control} name="name" placeholder="Name"/>
                    <InputField control={form.control} name="weight" placeholder="Weight"/>
                    <InputField control={form.control} name="content_value_cents" type="number" step="0.01"
                                placeholder="Content Value"/>
                    <SelectField control={form.control} name="parcel_type" placeholder="Select Parcel Type"
                                 options={parcelTypes}/>

                    <div className="text-right">
                        <Button type="submit"
                                className="w-full">Submit</Button>
                    </div>
                </form>
            </Form>
        </div>
    )
}