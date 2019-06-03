/**
 * Developed by the Google team
 * Except as otherwise noted, the code samples are licensed under the Apache 2.0 License. 
 * For details, see https://developers.google.com
 */

// The Complete end-to-end example using the Google Pay API JavaScript Library
// Adapted from https://developers.google.com/pay/api/wed/guides/tutorial
// if within markup, place this under one script

/**
 * Define the version of the Google Pay API referenced when creating your configuration
 * @see {@link https://developers.google.com/pay/api/web/reference/object#PaymentDataRequest|apiVersion in PaymentDataRequest}
 */
const baseRequest = {
    apiVersion: 2,
    apiVersionMinor: 0
};

/**
 * Card networks supported by your site and your gateway
 * @see {@link https://developers.google.com/pay/api/web/reference/object#CardParameters|CardParameters}
 * @todo confirm card networks supported by your site and gateway
 */
const allowedCardNetworks = ["AMEX","DISCOVER","JCB","MASTERCARD","VISA"];

/**
 * Card authentication methods supported by your site and your gateway
 * @see {@link https://developers.google.com/pay/api/web/reference/object#CardParameters|CardParameters}
 * @todo confirm your processor supports Android device tokens for your supported card networks
 */
const allowedCardAuthMethods = ["PAN_ONLY","CRYPTOGRAM_3DS"];

/**
 * Identify your gateway and your site's gateway merchant identifier
 * (The Google Pay API response will return an encrypted payment method capable
 * of being charged by a supported gateway after payer authorization)
 * @see {@link https://developers.google.com/pay/api/web/reference/object#Gateway|PaymentMethodTokenizationSpecification}
 * @todo check with your gateway on the parameters to pass
 */
const tokenizationSpecification = {
    type: 'PAYMENT_GATEWAY',
    parameters: {
        'gateway': 'example',
        'gatewayMerchantId': 'exampleGatewayMerchantId'
    }
};

/**
 * Descrice your site's support for the CARD payment method and it's required fields
 * @see {@link https://developers.google.com/pay/api/web/reference/object#CardParameters|CardParameters}
 */
const baseCardPaymentMethod = {
    type: 'CARD',
    parameters: {
        allowedAuthMethods: allowedCardAuthMethods,
        'allowedCardNetworks': allowedCardNetworks
    }
};

/**
 * Describe your site's support for the CARD payment method including optional fields
 * @see {@link https://developers.google.com/pay/api/web/reference/object#CardParameters|CardParameters}
 */
const cardPaymentMethod = Object.assign(
    {},
    baseCardPaymentMethod,
    {
        tokenizationSpecification: tokenizationSpecification
    }
);

/**
 * An initialized google.payments.api.PaymentsClient object or null if not yet set
 * @see {@link getGooglePaymentsClient}
 */
let paymentsClient = null;

/**
 * Configure your site's support for payment methods supported by the Google Pay API
 * (Each member of allowedPaymentMethods should contain only the required fields,
 * allowing reuse of this base request when determining a viewer's ability
 * to pay and later requesting a supported payment method)
 * @returns {object} Google Pay API version, payment methods supported by the site
 */
function getGoogleIsReadyToPayRequest() {
    return Object.assign(
        {},
        baseRequest,
        {
            allowedPaymentMethods: [baseCardPaymentMethod]
        }
    );
}

/**
 * Configure support for the Google Pay API
 * @see {@link https://developers.google.com/pay/api/web/reference/object#PaymentDataRequest|PaymentDataRequest}
 * @returns {object} PaymentDataRequest fields
 */
function getGooglePaymentDataRequest() {
    const PaymentDataRequest = Object.assign({}, baseRequest);
    PaymentDataRequest.allowedPaymentMethods = [cardPaymentMethod];
    PaymentDataRequest.transactionInfo = getGoogleTransactionInfo();
    PaymentDataRequest.merchantInfo = {
        /**
         * @todo a merchant ID is vailbale for a production environment after approval by Google
         * See {@link https://developers.google.com/pay/api/web/guides/test-and-deploy/integration-checklist|Integration checklist}
         * merchantId: '01234567890123456789',
         */
        merchantName: 'Example Merchant'
    };
    return PaymentDataRequest;
}

/**
 * Return an active PaymentsClient or initialize
 * @see {@link https://developers.google.com/pay/api/web/reference/client#PaymentsClient|PaymentsClient construct}
 * @returns {google.payments.api.PaymentsClient} Google Pay API Client
 */
function getGooglePaymentsClient() {
    if (paymentsClient === null) {
        paymentsClient = new google.payments.api.PaymentsClient({environment: 'TEST'});
    }
    return paymentsClient;
}

/**
 * Initialize Google PaymentsClient after google-hosted JavaScript has loaded
 * Display a Google Pay payment button after confirmation of the viewer's ability to pay
 */
function onGooglePayLoaded() {
    const paymentsClient = getGooglePaymentsClient();
    paymentsClient.isReadyToPay(getGoogleIsReadyToPayRequest())
        .then(function(response) {
            if (response.result) {
                addGooglePayButton();
                /**
                 * @todo prefetch payment data to improve performance after confirming site functionality
                 */
                prefetchGooglePaymentData();
            }
        })
        .catch(function(err) {
            // show error in developer console for debugging
            console.error(err);
        });
}

/**
 * Add a Google Pay purchase button alongside an existing checkout button
 * @see {@link https://developers.google.com/pay/api/web/reference/object#ButtonOptions|Button options}
 * @see {@link https://developers.google.com/pay/api/web/guides/brand-guidelines|Google Pay brand guidelines}
 */
function addGooglePayButton() {
    const paymentsClient = getGooglePaymentsClient();
    const button = paymentsClient.createButton(
        {onClick: onGooglePaymentButtonClicked, buttonColor: 'black', buttonType: 'short'}
    );
    // Remember to customize this id="container" to match where you place this button
    document.getElementById('container').appendChild(button);
}

/**
 * Provide Gooogle Pay API with a payment amount, currency, and amount status
 * @see {@link https://developers.google.com/pay/api/web/reference/object#TransactionInfo|TransactionInfo}
 * @returns {object} transaction info, suitable for use as transactionInfo property of PaymentDataRequest
 */
function getGoogleTransactionInfo() {
    return {
        currencyCode: 'USD',
        totalPriceStatus: 'FINAL',
        // set to cart total
        totalPrice: '1.00'
    };
}

/**
 * Prefetch payment data to improve performance
 * @see {@link https://developers.google.com/apy/api/web/reference/client#prefetchPaymentData|prefetchPaymentData()}
 */
function prefetchGooglePaymentData() {
    const PaymentDataRequest = getGooglePaymentDataRequest();
    // transactionInfo must be set but does not affect cache
    PaymentDataRequest.transactionInfo = {
        totalPriceStatus: 'NOT_CURRENTLY_KNOWN',
        currencyCode: 'USD'
    };
    const paymentsClient = getGooglePaymentsClient();
    paymentsClient.prefetchPaymentData(PaymentDataRequest);
}

/**
 * Show Google Pay payment sheet when Google Pay payment button is clicked
 */
function onGooglePaymentButtonClicked() {
    const PaymentDataRequest = getGooglePaymentDataRequest();
    PaymentDataRequest.transactionInfo = getGoogleTransactionInfo();

    const paymentsClient = getGooglePaymentsClient();
    paymentsClient.loadPaymentData(PaymentDataRequest)
        .then(function(paymentData) {
            // handle the response
            processPayment(paymentData);
        })
        .catch(function(err) {
            // show error in developer console for debugging
            console.error(err);
        });
}

/**
 * Process payment data returneed by the Google Pay API
 * @param {object} paymentData response from Google Pay API after user approves payment 
 * @see {@link https://developers.google.com/pay/api/web/reference/object#PaymentData|PaymentData object reference}
 */
function processPayment(paymentData) {
    // show returned data in developer console for debugging
    console.log(paymentData);
    // @todo pass payment token to your gateway to process payment
    paymentToken = paymentData.paymentMethodData.tokenizationData.token;
}


/**
 * Place the following within your cart page
 * 
 * -- markup
 * <div id="container"></div> -- you can customize this id, and call it in the addGooglePayButton()
 * -- js
 * <script async src="https://pay.google.com/gp/p/js/pay.js" onLoad="onGooglePayLoaded()"></script>
 * 
 */

