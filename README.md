# Django_e-comerce_with_payment_getway_and_rest_api


### To run it in docker 
```bash
 bash scripts/live_server_deploy.sh 
```

### API Documentation (REST API)

#### 1. **Login API**
**URL:** `POST /api/login/`  
**Description:** Authenticates user and generates a session.  
**Request:**
- Header: `Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>`
- Form Data: 
  - `username` (string) - User's username
  - `password` (string) - User's password  

**Curl Example:**
```bash
curl --location 'http://127.0.0.1:8000/api/login/' \
--header 'Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>' \
--form 'username="admin"' \
--form 'password="1516"'
```

#### 2. **Create Thread API**
**URL:** `POST /api/threads/`  
**Description:** Creates a new thread.  
**Request:**
- Header: 
  - `Authorization: Bearer <JWT token>`
  - `Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>`
- Form Data:
  - `user` (integer) - User ID of the thread creator  

**Curl Example:**
```bash
curl --location 'http://127.0.0.1:8000/api/threads/' \
--header 'Authorization: Bearer <JWT token>' \
--header 'Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>' \
--form 'user="2"'
```

#### 3. **Register API**
**URL:** `POST /api/register/`  
**Description:** Registers a new user.  
**Request:**
- Header: 
  - `Authorization: Bearer <JWT token>`
  - `Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>`
- Form Data:
  - `username` (string) - New user's username
  - `email` (string) - New user's email
  - `password1` (string) - User's password
  - `password2` (string) - Password confirmation  

**Curl Example:**
```bash
curl --location 'http://127.0.0.1:8000/api/register/' \
--header 'Authorization: Bearer <JWT token>' \
--header 'Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>' \
--form 'username="admin1"' \
--form 'email="itsmahadi@gmail.com"' \
--form 'password1="M@h@d\!@199610"' \
--form 'password2="M@h@d\!@199610"'
```

#### 4. **Request Email Verification API**
**URL:** `POST /api/request_by_email_verification/`  
**Description:** Requests an email verification for a specific action.  
**Request:**
- Header: `Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>`
- Form Data:
  - `email` (string) - User's email
  - `using_for` (string) - Purpose (e.g., `password_reset`)

**Curl Example:**
```bash
curl --location 'http://127.0.0.1:8000/api/request_by_email_verification/' \
--header 'Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>' \
--form 'email="itsmahadi@gmail.com"' \
--form 'using_for="password_reset"'
```

#### 5. **Verify Email Token API**
**URL:** `POST /api/verify_email_token/`  
**Description:** Verifies the OTP sent to the user's email.  
**Request:**
- Header: `Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>`
- Form Data:
  - `otp` (string) - OTP sent to the user's email
  - `email` (string) - User's email
  - `using_for` (string) - Purpose (e.g., `password_reset`)
  - `password` (string) - New password (for password reset)

**Curl Example:**
```bash
curl --location 'http://127.0.0.1:8000/api/verify_email_token/' \
--header 'Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>' \
--form 'otp="2285"' \
--form 'email="itsmahadi@gmail.com"' \
--form 'using_for="password_reset"' \
--form 'password="M@h@d\!@1996"'
```


#### 6. **Get Products API**
**URL:** `GET /api/products/`  
**Description:** Retrieves a list of products.  
**Request:**
- Header: 
  - `Authorization: Bearer <JWT token>`
  - `Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>`

**Curl Example:**
```bash
curl --location 'http://127.0.0.1:8000/api/products/' \
--header 'Authorization: Bearer <JWT token>' \
--header 'Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>'
```

#### 7. **Order Shipping API**
**URL:** `GET /api/order_shipping/`  
**Description:** Retrieves order shipping information.  
**Request:**
- Header: 
  - `Authorization: Bearer <JWT token>`
  - `Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>`

**Curl Example:**
```bash
curl --location 'http://127.0.0.1:8000/api/order_shipping/' \
--header 'Authorization: Bearer <JWT token>' \
--header 'Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>'
```

#### 8. **Product Cart API (Add or Modify Cart Items)**
**URL:** `POST /api/product_cart/`  
**Description:** Adds a product to the cart.  
**Request:**
- Header: 
  - `Authorization: Bearer <JWT token>`
  - `Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>`

**Curl Example:**
```bash
curl --location 'http://127.0.0.1:8000/api/product_cart/' \
--header 'Authorization: Bearer <JWT token>' \
--header 'Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>'
```

#### 9. **Product Cart Item API (Supports POST, PATCH, PUT, DELETE)**
**URL:** `/api/product_cart/{id}/`  
**Description:** Allows modification of a cart item. Supports creating, updating, or deleting a cart item.  
**Request:**
- Header: 
  - `Authorization: Bearer <JWT token>`
  - `Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>`
- Form Data (for POST/PUT/PATCH):
  - `cart` (integer) - Cart ID
  - `product` (integer) - Product ID
  - `created_by` (integer) - User ID who created the cart
  - `quantity` (integer) - Quantity of the product

**Curl Example:**
- **POST/PUT/PATCH:**
```bash
curl --location 'http://127.0.0.1:8000/api/product_cart/11/' \
--header 'Authorization: Bearer <JWT token>' \
--header 'Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>' \
--form 'cart="7"' \
--form 'product="5"' \
--form 'created_by="1"' \
--form 'quantity="7"'
```
- **DELETE:**
```bash
curl --location --request DELETE 'http://127.0.0.1:8000/api/product_cart/11/' \
--header 'Authorization: Bearer <JWT token>' \
--header 'Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>'
```


#### 10. **Aamar Pay Payment Request API**

**URL:** `POST /api/aamar_pay_payment_request/`  
**Description:** Initiates a payment request via Aamar Pay and returns a URL that the user can open in a browser to proceed with the payment.

#### **Request:**
- **Headers:**
  - `Authorization: Bearer <JWT token>`
  - `Content-Type: application/json`
  - `Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>`
  
- **Body (JSON):**
  - `cus_name` (string) - Customer's name
  - `cus_email` (string) - Customer's email
  - `cus_phone` (string) - Customer's phone number
  - `currency` (string) - Currency code (e.g., `BDT` for Bangladeshi Taka)
  - `success_url` (string) - URL to redirect after successful payment
  - `fail_url` (string) - URL to redirect after failed payment
  - `cancel_url` (string) - URL to redirect if payment is canceled
  - `cus_add1` (string) - Customer's address line 1
  - `cus_add2` (string) - Customer's address line 2
  - `cus_city` (string) - Customer's city
  - `cus_state` (string) - Customer's state
  - `cus_postcode` (string) - Customer's postal code
  - `cus_country` (string) - Customer's country
  - `type` (string) - Response format, usually `json`
  - `desc` (string) - Description of the payment
  - `identification` (object) - Additional identification info
    - `cart_id` (integer) - Cart ID associated with the payment

#### **Curl Example:**
```bash
curl --location 'http://127.0.0.1:8000/api/aamar_pay_payment_request/' \
--header 'Authorization: Bearer <JWT token>' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=<csrftoken>; sessionid=<sessionid>' \
--data-raw '{
    "cus_name": "Mahadi",
    "cus_email": "me.mahadi10@gmail.com",
    "cus_phone": "01715059172",
    "currency": "BDT",
    "success_url": "http://127.0.0.1:8000/api/aamar_pay_payment_confirmation_request/",
    "fail_url": "http://127.0.0.1:8000/api/aamar_pay_payment_confirmation_fail_request/",
    "cancel_url": "http://127.0.0.1:8000/api/aamar_pay_payment_confirmation_fail_request/",
    "cus_add1": "dhaka",
    "cus_add2": "dhaka",
    "cus_city": "dhaka",
    "cus_state": "dhaka",
    "cus_postcode": "1216",
    "cus_country": "bangladesh",
    "type": "json",
    "desc": "Description",
    "identification": {
        "cart_id": 7
    }
}'
```

**Response:**  
Returns a payment URL to be opened in the browser for continuing the payment process.

**Stripe requires frontend library so i have did not implemented it**


# For better understanding please contact me, I can help you to understand the project.