# Catalog App

> Victor Lellis

A simple web application that provides:
- Third party user authentication and registration (Google / Facebook);
- Persisted data storage (SQLite);
- RESTful operations (Create, Read, Update and Delete) to categories and items;
- Authorization:
  - Only allowed to update or delete items and categories users who created them;
  - Users only can create category and item if logged.

## Pre-Requisites

- Download Vagrant and Virtual Box.
- Download or clone [fullstack-nanodegree-vm repository](https://github.com/udacity/fullstack-nanodegree-vm).
- Clone this repo into the `catlog/` directory.
- Runs the vm (`vagrant up`).
- Runs the terminal (`vagrant ssh`).

### Generating Google OAuth credentials

- Create a project on [developers.google.com](https://console.developers.google.com/).
- Go to "APIs and Services" -> "Credentials".
- Then select "Add Credentials" -> "OAuth (v2) token". Choose `Web` as the type.
- In the next page, make sure you have `http://localhost:5000` in authorized JavaScript origins and `http://localhost:5000` in Redirect URIs.
- Get your json client secret and save as `client_secrets.json`;
-

### Generating Facebook OAuth credentials

- Create a project on [developers.facebook.com](https://developers.facebook.com/).
- Go to "Products" -> "Facebook Login".
- Select "Web";
- Make sure you have `https://localhost:5000` in `Valid OAuth Redirect URIs`.
- Get `App ID` and the `App Secret` and create the file `fb_client_secrets.json`:

```
{
  "web": {
    "app_id": "PASTE_YOUR_APP_ID_HERE",
    "app_secret": "PASTE_YOUR_CLIENT_SECRET_HERE"
  }
}

```


## Getting started
- From the main directory run `sudo pip install -r requirements.txt`.
- Run the application with `python server.py`.
- Access on `http://localhost:5000`.

## Endpoints
### JSON Endpoints
- `/catalog.json` - JSON of all categories with items in catalog
- `/categories.json` - JSON of all categories
- `/items.json` - JSON of all items
- `/categories/<category_id>/items.json.json` - JSON of all items in category

### REST Endpoints
- `/` or `/catalog` - Catalog page with all categories and recently added items
- `/categories/new` - Create new category
- `/categories/<category_id>/edit` - Edit an existing category
- `/categories/<category_id>/delete` - Delete an existing category
- `/categories/<category_id>` or `/categories/<category_id>/items` - Items in category
- `/items/new` - Create new item
- `/categories/<category_id>/edit` - Edit an existing item
- `/categories/<category_id>/delete` - Delete an existing item

## Notes
- To use `Facebook Login` is required to run in SSL protocol (It's not possible to set Enforce HTTPS as NO).
- To run in ssl protocol, add `ssl_context='adhoc'` in `app.run` (`server.py`).

