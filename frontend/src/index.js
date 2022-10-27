import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import App from './App'
import reportWebVitals from './reportWebVitals'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import MyListings from './pages/UserPages/MyListings'
import MyProfile from './pages/MyProfile'
import NavBarComp from './components/NavBarComp'
import NewListings from './pages/UserPages/NewListings'
import EditProfile from './pages/UserPages/EditProfile'
import ChangePassword from './pages/ChangePassword'
import BookListingInformation from './pages/BookListingInformation'
import ForgetPassword from './pages/ForgetPassword'
import Register from './pages/UserPages/Register'
import EditListings from './pages/UserPages/EditListings'
import { SearchResult } from './pages/SearchResult'
import ViewOffers from './pages/UserPages/ViewOffers'
import MyOffers from './pages/UserPages/MyOffers'
import TransactionDetails from './pages/UserPages/TransactionDetails'
import ErrorPage from './pages/ErrorPage'
import ManageUsers from './pages/AdminPages/ManageUsers'
import ManageUsersResult from './pages/AdminPages/ManageUsersResult'
import ManageBooks from './pages/AdminPages/ManageBooks'
import ManageBooksResult from './pages/AdminPages/ManageBooksResult'
//Homepage is App.js, Navbar is NavbarComp.js

const root = ReactDOM.createRoot(document.getElementById('root'));

const isAuthenticated = localStorage.getItem("Authentication");
root.render(
  <React.StrictMode>
    <Router>
      <NavBarComp />
      <Routes>
        <Route index element={<App />} />
        <Route exact path='/' element={<App />} />
        <Route exact path='/Register' element={<Register />} />
        <Route exact path='/BookListingInformation' element={<BookListingInformation />} />
        <Route exact path='/SearchResult' element={<SearchResult />} />
        <Route path='*' element={<ErrorPage />} />

        {/* Common Routes */}
        <Route exact path='/MyProfile/ChangePassword' element={<ChangePassword />} />
        <Route exact path='/ForgetPassword' element={<ForgetPassword />} />
        <Route exact path='/MyProfile' element={<MyProfile />} />

        {/* User Routes */}
        <Route exact path='/MyOffers' element={<MyOffers />} />
        <Route exact path='/MyOffers/TransactionDetails' element={<TransactionDetails />} />
        <Route exact path='/MyListings' element={<MyListings />} />
        <Route exact path='/MyListings/NewListings' element={<NewListings />} />
        <Route exact path='/MyListings/EditListings' element={<EditListings />} />
        <Route exact path='/MyListings/ViewOffers' element={<ViewOffers />} />
        <Route exact path='/MyProfile/EditProfile' element={<EditProfile />} />


        {/* Admin Routes */}
        <Route exact path='/ManageUsers' element={<ManageUsers />} />
        <Route exact path='/ManageUsers/ManageUsersResult' element={<ManageUsersResult />} />
        <Route exact path='/ManageBooks' element={<ManageBooks />} />
        <Route exact path='/ManageBooks/ManageBooksResult' element={<ManageBooksResult />} />

      </Routes>
    </Router>
  </React.StrictMode>
);


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
