const Home = ({children}: { children: React.ReactNode }) => {
    return (
        <main className="h-full bg-[#111827] flex justify-center items-center">
            <div className="w-full max-w-screen-md mx-auto p-4">
                {children}
            </div>
        </main>
    )
}

export default Home