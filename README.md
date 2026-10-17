# Ceramic Membrane Material Science Calculator

This repository contains an automated calculator for ceramic membrane fabrication and characterization.
It standardizes raw material formulations, processes physical measurements before and after sintering using international standards
(ASTM C 373), calculates fluid dynamics properties, and classifies the resulting membrane structure.

---

## 1. Material Formulation Standardization
To ensure raw materials sum exactly to $100\%$, raw formulation entries are standardized mathematically:

$$\bar{x}_i = \frac{x_i \times 100}{\sum_{j} x_j}$$

Where:
- $x_i$ is the individual input proportion of raw material (Kaolin, Rice Husk, Calcite, Feldspar, Quartz).
- $\bar{x}_i$ is the normalized, standardized percentage.

---

## 2. Dimensional and Physical Properties (ASTM C 373)
After sintering, physical parameters are characterized using the liquid displacement method:

* **Dry Surface Area ($A_{\text{dry}}$):**
  $$A_{\text{dry}} = L_{\text{dry}} \times W_{\text{dry}}$$
* **Dry Volume ($V_{\text{dry}}$):**
  $$V_{\text{dry}} = L_{\text{dry}} \times T_{\text{dry}} \times W_{\text{dry}}$$
* **Linear Shrinkage ($S_L$):**
  $$S_L = \frac{L_{\text{dry}} - L_{\text{final}}}{L_{\text{dry}}}$$
* **Mass Loss ($M_{\text{loss}}$):**
  $$M_{\text{loss}} = \frac{m_{\text{dry}} - m_{\text{final}}}{m_{\text{dry}}}$$
* **Apparent Porosity (Open Porosity, $\epsilon$):**
  $$\epsilon (\%) = \frac{m_{\text{sat}} - m_{\text{dry}}}{m_{\text{sat}} - m_{\text{sus}}} \times 100$$
* **Water Absorption ($WA$):**
  $$WA (\%) = \frac{m_{\text{sat}} - m_{\text{dry}}}{m_{\text{dry}}} \times 100$$
* **Relative Density ($RD$):**
  $$RD (\%) = \frac{\rho_{\text{bulk}}}{\rho_{\text{theoretical}}} \times 100$$
* **Total Porosity ($P_{\text{total}}$):**
  $$P_{\text{total}} (\%) = 100 - RD$$

---

## 3. Membrane Performance Analysis

### Water Permeability ($K_w$)
Permeability is modeled using Darcy's Law:

$$K_w = \frac{Q \cdot \eta \cdot T_{\text{membrane}}}{\Delta P}$$

Where:
- $Q$ is the volumetric flow rate (mL/hour).
- $\eta$ is the liquid viscosity (cP).
- $T_{\text{membrane}}$ is the final membrane thickness (mm).
- $\Delta P$ is the operating pressure difference (bar).

### Average Pore Size ($r_{\text{avg}}$)
Estimated using the modified **Guerout-Elford-Ferry Equation** for porous systems:

$$r_{\text{avg}} = \frac{\sqrt{(2.9 - 1.75\epsilon) \cdot 8 \cdot \eta \cdot T_{\text{membrane}} \cdot Q}}{\epsilon \cdot A_{\text{membrane}} \cdot \Delta P}$$

Where:
- $\epsilon$ is the fractional apparent porosity ($0 \le \epsilon \le 1$).
- $A_{\text{membrane}}$ is the active membrane filtration area (mm$^2$).

---

## 4. IUPAC Classification of Porous Membranes
Based on the computed average pore size, the membrane is classified into three categories:
1. **Macroporous:** Pore size $> 50.0$ microns $\rightarrow$ Ideal for **Microfiltration**.
2. **Mesoporous:** $2.0 <$ Pore size $\le 50.0$ microns $\rightarrow$ Ideal for **Microfiltration**.
3. **Microporous:** Pore size $\le 2.0$ microns $\rightarrow$ Ideal for **Ultrafiltration**.

---

## Repository Purpose
This project is intended to turn the Colab-based ceramic membrane calculations into a reusable, versioned, and testable Python project.

## Planned Structure
- `src/` — calculator logic
- `tests/` — validation and unit tests
- `examples/` — sample input/output workflows
- `README.md` — project overview and formula references
