## Mobile Flows – Purchase Journey in the Americanas App  
## 🎯 Objective

### Validate the complete product purchase flow in the Americanas mobile app, using the 3 products returned from the `wishlist` of the `project_final` API.
The test ensures that the information displayed (name, price, and shipping) is correct and that the purchase process works properly up to the checkout screen.

🧾 **Scenario Summary**

- Open the Americanas app.  
- Search for a product returned by the API wishlist.  
- Select the correct product from the results.  
- Validate the product page:  
  - Name and price match the API response.  
  - Enter an invalid ZIP code and validate the error message.  
  - Enter the valid ZIP code from the API and validate shipping cost and delivery estimate.  
- Add the product to the cart.  
- Validate the cart popup:  
  - Name and price are correct.  
  - Increase quantity to 2 units and validate the update.  
  - Decrease to 1 unit and verify that the “–” button becomes disabled.  
  - Increase again to 2 units.  
- Proceed to the checkout screen.  
- Validate the final cart:  
  - Correct product name and quantity.  
  - Subtotal and total reflecting twice the unit price.  
  - The “Finalize Purchase” button shows the total price for two units.  
- Repeat invalid and valid ZIP code validations.  
- Continue to checkout.  
- Validate the redirect to the login screen with the message:  
  **“Enter your email to continue.”**
