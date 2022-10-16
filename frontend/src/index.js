import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import App from './App'
import reportWebVitals from './reportWebVitals'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import MyListings from './pages/MyListings'
import MyProfile from './pages/MyProfile'
import NavBarComp from './components/NavBarComp'
import NewListings from './pages/NewListings'
import EditProfile from './pages/EditProfile'
import ChangePassword from './pages/ChangePassword'
import BookListingInformation from './pages/BookListingInformation'
import ForgetPassword from './pages/ForgetPassword'
import Register from './pages/Register'
import EditListings from './pages/EditListings'
import { SearchResult } from './pages/SearchResult'
import ViewOffers from './pages/ViewOffers'
import MyOffers from './pages/MyOffers'

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
        {isAuthenticated ? <Route exact path='/MyOffers' element={<MyOffers />} /> : null}
        {isAuthenticated ? <Route exact path='/MyListings' element={<MyListings />} /> : null}
        {isAuthenticated ? <Route exact path='/MyListings/NewListings' element={<NewListings />} /> : null}
        {isAuthenticated ? <Route exact path='/MyListings/EditListings' element={<EditListings />} /> : null}
        {isAuthenticated ? <Route exact path='/MyListings/ViewOffers' element={<ViewOffers />} /> : null}
        {isAuthenticated ? <Route exact path='/MyProfile' element={<MyProfile />} /> : null}
        {isAuthenticated ? <Route exact path='/MyProfile/EditProfile' element={<EditProfile />} /> : null}
        {isAuthenticated ? <Route exact path='/MyProfile/ChangePassword' element={<ChangePassword />} /> : null}
        {isAuthenticated ? <Route exact path='/ForgetPassword' element={<ForgetPassword />} /> : null}
      </Routes>
    </Router>
  </React.StrictMode>
);


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
