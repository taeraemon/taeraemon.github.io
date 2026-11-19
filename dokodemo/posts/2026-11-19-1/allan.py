"""Simulate a gyro with ARW + bias instability + RRW and draw the post's figures.

python3 allan.py   ->  adev.png, noise_types.png, clusters.png, filter.png next to this file
"""
import pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(3)  # one 24 h realization; long-tau points vary a lot between seeds
fs, hours = 50.0, 24
n = int(fs * 3600 * hours)
dt = 1 / fs

# true parameters (deg, s units)
N = 0.2 / 60            # ARW  0.2 deg/sqrt(h)  -> deg/sqrt(s)
B = 5.0 / 3600          # bias instability 5 deg/h -> deg/s
K = 20.0 / 3600 / 60    # RRW 20 deg/h/sqrt(h)  -> deg/s/sqrt(s)

white = N * np.sqrt(fs) * rng.standard_normal(n)

# flicker (1/f) noise: two-sided PSD B^2/(2 pi f), i.e. one-sided B^2/(pi f) (IEEE 952 convention)
f = np.fft.rfftfreq(n, dt)
spec = np.fft.rfft(rng.standard_normal(n))
scale = np.zeros_like(f)
scale[1:] = np.sqrt(B**2 / (np.pi * f[1:]) * fs / 2)
flicker = np.fft.irfft(spec * scale, n)

rrw = np.cumsum(K * np.sqrt(dt) * rng.standard_normal(n))

omega = white + flicker + rrw          # deg/s


def adev(omega, fs, n_tau=60):
    """Overlapping Allan deviation (IEEE Std 952)."""
    theta = np.concatenate([[0.0], np.cumsum(omega) / fs])
    m = np.unique(np.logspace(0, np.log10(len(omega) // 10), n_tau).astype(int))
    tau = m / fs
    sig = np.empty(len(m))
    for i, mi in enumerate(m):
        d = theta[2 * mi:] - 2 * theta[mi:-mi] + theta[:-2 * mi]
        sig[i] = np.sqrt(np.mean(d**2) / (2 * tau[i] ** 2))
    return tau, sig


tau, sig = adev(omega, fs)

# read the parameters back off the curve
N_curve = np.interp(0, np.log10(tau), sig)               # curve value at tau = 1 s (slightly high)
short = tau < 0.1                                        # region where the -1/2 slope dominates
N_hat = np.median(sig[short] * np.sqrt(tau[short]))      # -1/2 line evaluated at tau = 1 s
B_hat = sig.min() / np.sqrt(2 * np.log(2) / np.pi)       # flat bottom / 0.664
long = tau > 2000                                        # region where the +1/2 slope dominates
K_hat = np.median(sig[long] * np.sqrt(3 / tau[long]))    # extend that line back to tau = 3 s
print(f"N  true {N*60:.3f}  read {N_hat*60:.3f} deg/sqrt(h)  (curve at 1 s: {N_curve*60:.3f})")
print(f"B  true {B*3600:.2f}  read {B_hat*3600:.2f} deg/h")
print(f"K  true {K*3600*60:.2f}  read {K_hat*3600*60:.2f} deg/h/sqrt(h)")

to_h = 3600  # plot in deg/h
fig, ax = plt.subplots(figsize=(7, 4.6), dpi=150)
L = len(omega)
delta = 1 / np.sqrt(2 * (L / (tau * fs) - 1))           # rough relative error (El-Sheimy 2008)
ax.fill_between(tau, sig * (1 - delta) * to_h, sig * (1 + delta) * to_h, color="0.6", alpha=0.35, lw=0,
                label=r"$\pm\delta$ estimation uncertainty")
ax.loglog(tau, sig * to_h, "k", lw=2, label="Allan deviation (simulated)")
t = np.logspace(-2, 4.5, 50)
ax.loglog(t, N / np.sqrt(t) * to_h, "--", c="#1b6fb5", label=r"ARW  $N/\sqrt{\tau}$  (slope $-1/2$)")
ax.loglog(t, 0 * t + 0.664 * B * to_h, "--", c="#d1495b", label=r"Bias instability  $0.664B$  (slope 0)")
ax.loglog(t, K * np.sqrt(t / 3) * to_h, "--", c="#2a9d8f", label=r"RRW  $K\sqrt{\tau/3}$  (slope $+1/2$)")
ax.plot(1, N * to_h, "o", c="#1b6fb5")
ax.plot(3, K * to_h, "o", c="#2a9d8f")
ax.set(xlabel=r"$\tau$ [s]", ylabel=r"$\sigma(\tau)$ [deg/h]", xlim=(1e-2, 3e4), ylim=(0.2, 300))
ax.grid(True, which="both", alpha=0.25)
ax.legend(fontsize=8.5, loc="upper right")
fig.tight_layout()
fig.savefig(pathlib.Path(__file__).with_name("adev.png"))


# ---- second figure: what each noise looks like in time (-> noise_types.png) ----
r = np.random.default_rng(1)
fs2, T = 10.0, 2 * 3600
t2 = np.arange(int(fs2 * T)) / fs2
runs = 30

fig, axs = plt.subplots(3, 1, figsize=(7, 8), dpi=150, sharex=True)

# (a) ARW: integrate white rate noise -> angle spreads like N*sqrt(t)
ang = np.cumsum(N * np.sqrt(fs2) * r.standard_normal((runs, t2.size)), axis=1) / fs2
axs[0].plot(t2 / 60, ang.T, lw=0.6, alpha=0.5)
axs[0].plot(t2 / 60, N * np.sqrt(t2), "k--", t2 / 60, -N * np.sqrt(t2), "k--", lw=1.2)
axs[0].set(title="(a) ARW: angle error", ylabel="angle [deg]")

# (b) bias instability: the bias wanders but does not run away
nb = t2.size
fb = np.fft.rfftfreq(nb, 1 / fs2)
sb = np.zeros_like(fb)
sb[1:] = np.sqrt(B**2 / (np.pi * fb[1:]) * fs2 / 2)
bias = np.fft.irfft(np.fft.rfft(r.standard_normal(nb)) * sb, nb)
k = int(30 * fs2)  # 30 s moving average so the slow part is visible
axs[1].plot(t2[k - 1:] / 60, np.convolve(bias, np.ones(k) / k, "valid") * 3600, "#d1495b", lw=1)
axs[1].set(title="(b) Bias instability: bias (30 s moving average)", ylabel="bias [deg/h]")

# (c) RRW: the bias itself random-walks -> spreads like K*sqrt(t)
rw = np.cumsum(K / np.sqrt(fs2) * r.standard_normal((runs, t2.size)), axis=1)
axs[2].plot(t2 / 60, rw.T * 3600, lw=0.6, alpha=0.5)
axs[2].plot(t2 / 60, K * np.sqrt(t2) * 3600, "k--", t2 / 60, -K * np.sqrt(t2) * 3600, "k--", lw=1.2)
axs[2].set(title="(c) RRW: bias", xlabel="time [min]", ylabel="bias [deg/h]")

for a in axs:
    a.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(pathlib.Path(__file__).with_name("noise_types.png"))


# ---- third figure: cluster averages for short vs long tau (-> clusters.png) ----
# toy signal (arbitrary units): fast white noise + slow random-walk drift
r = np.random.default_rng(7)
fs3, T3 = 5.0, 600
t3 = np.arange(int(fs3 * T3)) / fs3
x = r.standard_normal(t3.size) + np.cumsum(r.standard_normal(t3.size)) * 0.03

fig, axs = plt.subplots(2, 1, figsize=(7, 5.2), dpi=150, sharex=True, sharey=True)
for a, tc, col in zip(axs, [10, 100], ["#1b6fb5", "#d1495b"]):
    a.plot(t3, x, c="0.75", lw=0.5)
    mc = int(tc * fs3)
    means = x[: len(x) // mc * mc].reshape(-1, mc).mean(1)
    starts = np.arange(len(means)) * tc
    a.hlines(means, starts, starts + tc, colors=col, lw=2.5)
    # black vertical segments = differences between neighbouring cluster means
    a.vlines(starts[1:], means[:-1], means[1:], colors="k", lw=1.6)
    if tc == 100:
        k = np.argmax(np.abs(np.diff(means)))
        a.annotate(r"$\Delta = \bar\Omega_{k+1}-\bar\Omega_k$", xy=(starts[k + 1], means[k:k + 2].mean()),
                   xytext=(starts[k + 1] + 25, 2.6), fontsize=10, arrowprops=dict(arrowstyle="->", lw=1))
    d = np.diff(means)
    a.set_title(rf"$\tau$ = {tc} s:  {len(means)} clusters,  "
                rf"$\sigma(\tau)=\sqrt{{\frac{{1}}{{2}}\overline{{\Delta^2}}}}$ = {np.sqrt(0.5 * np.mean(d**2)):.2f}",
                fontsize=10)
    a.set_ylim(-4, 4)
    a.set_ylabel("rate [arb.]")
    a.grid(alpha=0.25)
axs[1].set_xlabel("time [s]")
fig.tight_layout()
fig.savefig(pathlib.Path(__file__).with_name("clusters.png"))


# ---- fourth figure: the Allan "filter" moves with tau (-> filter.png) ----
fq = np.logspace(-4, 1, 2000)
fig, ax = plt.subplots(figsize=(7, 3.4), dpi=150)
for tc, col in zip([1, 10, 100, 1000], ["#1b6fb5", "#2a9d8f", "#e9a23b", "#d1495b"]):
    xx = np.pi * fq * tc
    ax.semilogx(fq, np.sin(xx) ** 4 / xx**2, c=col, lw=1.8, label=rf"$\tau$ = {tc} s")
    ax.axvline(0.371 / tc, c=col, ls=":", lw=1)
ax.set(xlabel="frequency $f$ [Hz]", ylabel=r"$\sin^4(\pi f\tau)\,/\,(\pi f\tau)^2$", xlim=(1e-4, 10))
ax.grid(alpha=0.25, which="both")
ax.legend(fontsize=8.5)
fig.tight_layout()
fig.savefig(pathlib.Path(__file__).with_name("filter.png"))
