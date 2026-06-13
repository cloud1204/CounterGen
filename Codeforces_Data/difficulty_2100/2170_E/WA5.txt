#include <bits/stdc++.h>
using namespace std;

int n, m;
int arr[300005];
long long dp[300005];

const long long mod = 998244353;

void solve() {
	cin >> n >> m;
	for (int i = 0; i < n; i++) arr[i] = -1;
	for (int i = 0; i < m; i++) {
		int l, r;
		cin >> l >> r;
		arr[r] = max(arr[r], l);
	}
	dp[0] = 1;
	int latest = -1;
	for (int i = 1; i <= n; i++) {
		dp[i] = 2 * dp[i - 1];
		dp[i] %= mod;
		if (arr[i] <= latest) continue;
		if (latest + 1 == arr[i]) dp[i] -= dp[arr[i] - 1];
		else dp[i] -= dp[arr[i] - 1] * 2;
		dp[i] %= mod;
		dp[i] += mod;
		dp[i] %= mod;

		latest = arr[i];
	}
	cout << dp[n] << endl;
}

int main() {
	istream::sync_with_stdio(0);
	cin.tie(nullptr);
	int t;
	cin >> t;
	while (t--) {
		solve();
	}
	return 0;
}