import {PaymentScreen} from "@point_of_sale/app/screens/payment_screen/payment_screen";
import {patch} from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    onMounted() {
        super.onMounted();
        const invoice_by_default = this.pos.config.invoice_by_default;
        if (invoice_by_default) {
            const order = this.pos.getOrder();
            order.setToInvoice(invoice_by_default);
        }
    },
});
