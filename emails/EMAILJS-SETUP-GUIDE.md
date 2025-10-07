# EmailJS Setup Guide for QULTURE

## Step-by-Step Instructions

### **STEP 1: Create EmailJS Account**

1. Go to **[https://emailjs.com](https://emailjs.com)**
2. Click **"Sign Up"** (top right)
3. Fill in:
   - Email: `dissismyemail@gmail.com`
   - Password: (create a secure password)
   - Name: Shems / QULTURE
4. Click **"Create Account"**
5. Check your email (`dissismyemail@gmail.com`) and verify your account

---

### **STEP 2: Add Email Service**

1. Once logged in, go to **"Email Services"** in the left sidebar
2. Click **"Add New Service"**
3. Choose **"Gmail"**
4. Click **"Connect Account"**
5. Sign in with your Google account (`dissismyemail@gmail.com`)
6. Allow EmailJS to send emails on your behalf
7. **IMPORTANT:** Copy your **Service ID** (looks like `service_abc1234`)
   - Save it somewhere - you'll need it later!

---

### **STEP 3: Create Template #1 - Admin Order Notification**

1. Go to **"Email Templates"** in the left sidebar
2. Click **"Create New Template"**
3. Fill in the template:

**Template Name:** `order_notification`

**Subject:** 
```
New QULTURE Order - {{order_id}}
```

**Content (Body):**
```
New Order Received!

Order ID: {{order_id}}
Storefront: {{storefront}}
Order Date: {{order_date}}

CUSTOMER DETAILS:
Name: {{customer_name}}
Email: {{customer_email}}
Phone: {{customer_phone}}

SHIPPING ADDRESS:
{{customer_address}}

ORDER ITEMS:
{{items}}

Subtotal: {{subtotal}}
Notes: {{notes}}

---
QULTURE Order Management
Contact: {{to_email}}
```

4. **To Email:** Leave blank (we'll set it dynamically)
5. **From Name:** `QULTURE Orders`
6. Click **"Save"**
7. **IMPORTANT:** Copy the **Template ID** (top of the page, looks like `template_abc1234`)

---

### **STEP 4: Create Template #2 - Customer Confirmation**

1. Still in **"Email Templates"**, click **"Create New Template"**
2. Fill in:

**Template Name:** `customer_confirmation`

**Subject:**
```
Your QULTURE Order Confirmation - {{order_id}}
```

**Content (Body):**
```
Hi {{to_name}},

Thank you for your QULTURE order! We're excited to get your hoodie to you.

ORDER DETAILS:
Order ID: {{order_id}}

ITEMS:
{{items}}

Total: {{subtotal}}
Estimated Shipping: {{estimated_shipping}}

We'll send you a shipping confirmation once your order is on its way.

Questions? Contact us:
Email: {{contact_email}}
Phone: {{contact_phone}}

Thanks for supporting QULTURE!
- The QULTURE Team

---
Wear the icebreaker. Connect through conversation.
```

3. **From Name:** `QULTURE`
4. Click **"Save"**
5. **IMPORTANT:** Copy this **Template ID** as well

---

### **STEP 5: Get Your Public Key**

1. Go to **"Account"** in the left sidebar
2. Click **"General"**
3. Find the **"Public Key"** section
4. **IMPORTANT:** Copy your **Public Key** (looks like `ABC12xyz_456`)

---

### **STEP 6: Update Your Code**

Once you have all three credentials, send them to me:
- ✅ Service ID
- ✅ Template ID (order_notification)
- ✅ Template ID (customer_confirmation)  
- ✅ Public Key

And I'll update your `email-service.js` file with the correct values!

---

## Quick Reference - What Goes Where:

```javascript
this.serviceId = 'YOUR_SERVICE_ID';        // From Step 2
this.templateId = 'YOUR_TEMPLATE_ID';      // From Step 3 (order_notification)
this.publicKey = 'YOUR_PUBLIC_KEY';        // From Step 5
```

The customer confirmation template ID goes in line 71 of email-service.js.

---

## Need Help?

If you get stuck on any step, just let me know where you are and I'll help you through it!

---

## Testing Your Setup

Once everything is configured:
1. Go to your storefront (storefront.html)
2. Fill out an order
3. Submit it
4. Check dissismyemail@gmail.com for the order notification
5. The customer should also receive a confirmation email

---

**Let's do this! 🚀**

