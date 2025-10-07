// Email service for QULTURE storefront orders
// This handles sending order notifications and customer confirmations

class EmailService {
  constructor() {
    // EmailJS configuration - you'll need to set up a free account at emailjs.com
    this.serviceId = 'service_os67k8x'; // Replace with your EmailJS service ID
    this.templateId = 'template_liaswfr'; // Replace with your EmailJS template ID
    this.publicKey = '7qsqAbjhBHHBvkPLZ'; // Replace with your EmailJS public key
    
    // Your email where you'll receive order notifications
    this.adminEmail = 'dissismyemail@gmail.com';
    
    // Initialize EmailJS (you'll need to include the EmailJS script in your HTML)
    if (typeof emailjs !== 'undefined') {
      emailjs.init(this.publicKey);
    }
  }

  // Send order notification to admin (you)
  async sendOrderNotification(orderData) {
    const emailData = {
      to_email: this.adminEmail,
      to_name: 'QULTURE',
      order_id: this.generateOrderId(),
      customer_name: orderData.customer.name,
      customer_email: orderData.customer.email,
      customer_phone: orderData.customer.phone || 'Not provided',
      customer_address: this.formatAddress(orderData.customer),
      items: this.formatItems(orderData.items),
      subtotal: orderData.subtotal,
      notes: orderData.customer.notes || 'No notes',
      order_date: new Date().toLocaleString(),
      storefront: orderData.storefront || 'Original'
    };

    try {
      console.log('Attempting to send order notification...');
      console.log('EmailJS available:', typeof emailjs !== 'undefined');
      console.log('Service ID:', this.serviceId);
      console.log('Template ID:', this.templateId);
      console.log('Public Key:', this.publicKey);
      
      if (typeof emailjs !== 'undefined') {
        console.log('Sending email with EmailJS...');
        const result = await emailjs.send(this.serviceId, this.templateId, emailData);
        console.log('EmailJS result:', result);
        console.log('Order notification sent successfully');
        return true;
      } else {
        // Fallback: log to console and localStorage for manual processing
        console.log('EmailJS not available. Order data:', emailData);
        this.saveOrderLocally(emailData);
        return true;
      }
    } catch (error) {
      console.error('Failed to send order notification:', error);
      console.error('Error details:', error.message);
      this.saveOrderLocally(emailData);
      return false;
    }
  }

  // Send confirmation email to customer
  async sendCustomerConfirmation(orderData) {
    const emailData = {
      to_email: orderData.customer.email,
      to_name: orderData.customer.name,
      order_id: this.generateOrderId(),
      items: this.formatItems(orderData.items),
      subtotal: orderData.subtotal,
      estimated_shipping: '5-7 business days',
      contact_email: this.adminEmail,
      contact_phone: '+1 (480) 274-5159'
    };

    try {
      console.log('Attempting to send customer confirmation...');
      console.log('Customer email:', emailData.to_email);
      
      if (typeof emailjs !== 'undefined') {
        console.log('Sending customer confirmation with EmailJS...');
        const result = await emailjs.send(this.serviceId, 'template_6q31bug', emailData);
        console.log('Customer confirmation EmailJS result:', result);
        console.log('Customer confirmation sent successfully');
        return true;
      } else {
        console.log('EmailJS not available. Customer confirmation data:', emailData);
        return false;
      }
    } catch (error) {
      console.error('Failed to send customer confirmation:', error);
      console.error('Customer confirmation error details:', error.message);
      return false;
    }
  }

  // Generate a simple order ID
  generateOrderId() {
    const timestamp = Date.now().toString(36);
    const random = Math.random().toString(36).substr(2, 5);
    return `QULT-${timestamp}-${random}`.toUpperCase();
  }

  // Format customer address
  formatAddress(customer) {
    const parts = [
      customer.address1,
      customer.address2,
      `${customer.city}, ${customer.state} ${customer.zip}`
    ].filter(Boolean);
    return parts.join('\n');
  }

  // Format order items
  formatItems(items) {
    return items.map(item => 
      `${item.product} - Size: ${item.size} - Qty: ${item.qty} - $${item.price.toFixed(2)} each`
    ).join('\n');
  }

  // Save order locally as backup
  saveOrderLocally(orderData) {
    const orders = JSON.parse(localStorage.getItem('qultureOrders') || '[]');
    orders.push({
      ...orderData,
      timestamp: new Date().toISOString(),
      status: 'pending'
    });
    localStorage.setItem('qultureOrders', JSON.stringify(orders));
  }

  // Get all pending orders (for admin use)
  getPendingOrders() {
    const orders = JSON.parse(localStorage.getItem('qultureOrders') || '[]');
    return orders.filter(order => order.status === 'pending');
  }

  // Mark order as fulfilled
  markOrderFulfilled(orderId) {
    const orders = JSON.parse(localStorage.getItem('qultureOrders') || '[]');
    const order = orders.find(o => o.order_id === orderId);
    if (order) {
      order.status = 'fulfilled';
      order.fulfilled_at = new Date().toISOString();
      localStorage.setItem('qultureOrders', JSON.stringify(orders));
    }
  }
}

// Export for use in storefronts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = EmailService;
} else {
  window.EmailService = EmailService;
}
