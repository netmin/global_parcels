import {Navbar} from "@/components/Navbar";
import {CreateForm} from "@/components/CreateForm";
import Layout from "@/components/Layout";


const Home = () => {

    return (
        <Layout>
            <div className="h-full">
                <CreateForm/>
            </div>
        </Layout>
    )
}

export default Home