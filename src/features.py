import re
import math
import ipaddress
import numpy as np
from urllib.parse import urlparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from scipy import sparse
import pandas as pd
import tldextract


class URLFeatureExtractor:
    """Extract and combine multiple types of features from URLs."""

    # Keywords commonly found in phishing URLs
    PHISHING_KEYWORDS = ['login', 'verify', 'secure', 'account', 'update', 'bank', 'paypal']

    def __init__(self):
        """Initialize the feature extractor."""
        self.tfidf_vectorizer = None
        self.scaler = None

    def fit(self, urls):
        """
        Fit TF-IDF vectorizer and MinMaxScaler on training URLs.

        Args:
            urls: List or array of URL strings

        Returns:
            self
        """
        # Fit TF-IDF on character n-grams (3,5)
        self.tfidf_vectorizer = TfidfVectorizer(
            analyzer='char',
            ngram_range=(3, 5),
            max_features=1000,
            lowercase=True
        )
        self.tfidf_vectorizer.fit(urls)

        # Fit MinMaxScaler on structural features
        structural_features = self._extract_structural_features(urls)
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.scaler.fit(structural_features)

        return self

    def transform(self, urls):
        """
        Extract and combine all features for given URLs.

        Args:
            urls: List or array of URL strings

        Returns:
            scipy.sparse matrix with combined features (TF-IDF + scaled structural features)
        """
        if self.tfidf_vectorizer is None or self.scaler is None:
            raise ValueError("Extractor must be fit before transform. Call fit() first.")

        # TF-IDF features
        tfidf_features = self.tfidf_vectorizer.transform(urls)

        # Structural features
        structural_features = self._extract_structural_features(urls)
        scaled_structural = self.scaler.transform(structural_features)

        # Verify all scaled features are non-negative (required by MultinomialNB)
        if np.any(scaled_structural < 0):
            raise ValueError(
                f"Scaled features contain negative values (min: {scaled_structural.min()}). "
                "This violates MultinomialNB requirements."
            )

        # Convert scaled structural features to sparse matrix
        structural_sparse = sparse.csr_matrix(scaled_structural)

        # Combine features
        combined_features = sparse.hstack([tfidf_features, structural_sparse])

        return combined_features

    def fit_transform(self, urls):

        return self.fit(urls).transform(urls)

    def _extract_structural_features(self, urls):
        features = []

        for url in urls:
            feature_vector = []

            # 1. URL length
            feature_vector.append(len(url))

            # 2. Number of dots
            feature_vector.append(url.count('.'))

            # 3. Number of hyphens
            feature_vector.append(url.count('-'))

            # 4. Number of digits
            feature_vector.append(sum(1 for c in url if c.isdigit()))

            # 5. Presence of '@' symbol
            feature_vector.append(1 if '@' in url else 0)

            # 6. Presence of 'https://'
            feature_vector.append(1 if url.lower().startswith('https://') else 0)

            # 7. IP address detection
            feature_vector.append(1 if self._is_ip_address(url) else 0)

            # 8. Subdomain depth
            depth = self._get_subdomain_depth(url)
            feature_vector.append(depth)

            # 9. Number of keywords
            keyword_count = self._count_keywords(url)
            feature_vector.append(keyword_count)

            # 10. Shannon entropy of domain
            entropy = self._shannon_entropy(self._extract_domain(url))
            feature_vector.append(entropy)

            features.append(feature_vector)

        return np.array(features, dtype=np.float32)

    @staticmethod
    def _is_ip_address(url):
        try:
            parsed = urlparse(url if '://' in url else f'http://{url}')
            host = parsed.netloc or parsed.path.split('/')[0]
            # Remove port if present
            host = host.split(':')[0]
            # Try to parse as IP address
            ipaddress.ip_address(host)
            return True
        except ValueError:
            return False

    @staticmethod
    def _extract_domain(url):
        try:
            parsed = urlparse(url if '://' in url else f'http://{url}')
            domain = parsed.netloc or parsed.path.split('/')[0]
            return domain
        except Exception:
            return url

    @staticmethod
    def _get_subdomain_depth(url):
        try:
            parsed = urlparse(url if '://' in url else f'http://{url}')
            domain = parsed.netloc or parsed.path.split('/')[0]
            # Remove port if present
            domain = domain.split(':')[0]
            
            # Use tldextract to properly parse subdomain
            extracted = tldextract.extract(domain)
            subdomain = extracted.subdomain
            
            # Count subdomain levels (split by dots)
            if subdomain:
                depth = subdomain.count('.') + 1
            else:
                depth = 0
            
            return depth
        except Exception:
            return 0

    def _count_keywords(self, url):
        url_lower = url.lower()
        count = sum(1 for keyword in self.PHISHING_KEYWORDS if keyword in url_lower)
        return count

    @staticmethod
    def _shannon_entropy(domain):
        if not domain:
            return 0.0

        # Calculate frequency of each character
        char_counts = {}
        for char in domain:
            char_counts[char] = char_counts.get(char, 0) + 1

        # Calculate entropy
        entropy = 0.0
        length = len(domain)
        for count in char_counts.values():
            probability = count / length
            if probability > 0:
                entropy -= probability * math.log2(probability)

        return entropy


def load_data(train_path, val_path, test_path):
    train_df = pd.read_csv(train_path)
    val_df = pd.read_csv(val_path)
    test_df = pd.read_csv(test_path)

    X_train = train_df['URL'].values
    y_train = train_df['Label'].values

    X_val = val_df['URL'].values
    y_val = val_df['Label'].values

    X_test = test_df['URL'].values
    y_test = test_df['Label'].values

    return X_train, y_train, X_val, y_val, X_test, y_test


if __name__ == '__main__':
    # Example usage and testing
    print("Feature Extraction Testing\n")

    # Test on 3 example URLs
    test_urls = [
        'https://www.google.com/search',
        'http://www.paypal.com.verify-login.xyz/secure',
        'tr7.datahost84.org/rrca.php?id=12345'
    ]

    extractor = URLFeatureExtractor()

    print("Testing structural features extraction:\n")
    structural = extractor._extract_structural_features(test_urls)

    feature_names = [
        'URL Length',
        'Dot Count',
        'Hyphen Count',
        'Digit Count',
        'Has @',
        'Has HTTPS',
        'Is IP',
        'Subdomain Depth',
        'Keyword Count',
        'Shannon Entropy'
    ]

    for i, url in enumerate(test_urls):
        print(f"URL {i+1}: {url}")
        for j, name in enumerate(feature_names):
            print(f"  {name:20} = {structural[i, j]:8.4f}")
        print()

    # Now test full extraction with fit/transform
    print(" Full Feature Extraction (TF-IDF + Structural) \n")

    # Load data
    try:
        X_train, y_train, X_val, y_val, X_test, y_test = load_data(
            'data/processed/train.csv',
            'data/processed/val.csv',
            'data/processed/test.csv'
        )

        print(f"Loaded data:")
        print(f"  Train: {len(X_train)} URLs")
        print(f"  Val:   {len(X_val)} URLs")
        print(f"  Test:  {len(X_test)} URLs\n")

        # Fit extractor on training data
        print("Fitting feature extractor on training data...")
        extractor = URLFeatureExtractor()
        extractor.fit(X_train)
        print("  ✓ Fit complete\n")

        # Transform all datasets
        print("Transforming datasets...")
        X_train_features = extractor.transform(X_train)
        X_val_features = extractor.transform(X_val)
        X_test_features = extractor.transform(X_test)
        print(f"  ✓ Train features shape: {X_train_features.shape}")
        print(f"  ✓ Val features shape:   {X_val_features.shape}")
        print(f"  ✓ Test features shape:  {X_test_features.shape}\n")

        # Show example features for test URLs
        print("Example features for test URLs:")
        test_urls_simple = test_urls[:min(2, len(test_urls))]
        test_features = extractor.transform(test_urls_simple)
        for i, url in enumerate(test_urls_simple):
            print(f"  URL: {url}")
            print(f"    Total features: {test_features[i].nnz} non-zero (sparse)")
            print(f"    Shape: {test_features[i].shape}")

    except FileNotFoundError as e:
        print(f"Note: Data files not found in current directory. {e}")
        print("Running test with synthetic data...\n")

        # Test with synthetic data
        synthetic_urls = test_urls + [
            'https://github.com/user/repo',
            'http://evil-domain.tk/phishing',
            'https://secure.bank-login.xyz/account'
        ]

        extractor = URLFeatureExtractor()
        features = extractor.fit_transform(synthetic_urls)
        print(f"Synthetic data features shape: {features.shape}")
        print(f"Number of non-zero entries: {features.nnz}")
