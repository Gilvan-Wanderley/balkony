# Capital Cost Estimate Model

## How to Use
How to use the Capital Cost library
This example demonstrates how to calculate the cost of a centrifugal pump made of stainless steel using the PumpCost class from the Capital Cost library. The following steps explain how to use it properly.

* **Step 1**: Import the PumpCost Class <br>
The first step is to import the PumpCost class from the balkony.capital_cost library:<br>
```python
from balkony.capital_cost import PumpCost
```
</br>

* **Step 2**: Create an Instance of `PumpCost`<br>
Next, you need to create an instance of the `PumpCost` class. In the example, the pump is specified as being of the centrifugal type and made of stainless steel. These parameters are passed as arguments to the class constructor:
```python
pump = PumpCost(PumpCost.Type.Centrifugal, 
                PumpCost.Material.StainlessSteel)
```
</br>

* **Step 3**: Calculate the Bare Module Cost<br>
Now, you can calculate the bare module cost of the pump using the `bare_module` method. This method takes two parameters:<br>
  * **Power**: A numeric value representing the pump's power, in this case, 350 kW (units should follow the library's expected format).<br>
  * **Pressure**: A numeric value of operating pressure. In the example, the value 1.0 barg is used (units should follow the library's expected format).
```python
cost = pump.bare_module(350, 1)
```
</br>

* **Step 4**: Display the Cost<br>
Finally, the cost is stored in the `cost` variable, which has a `value` attribute. To display the calculated value, you can use the print function:

```python
print(f"Pump cost: {cost.value}")
```

## Equipments List
The table below presents a list of all equipment and the respective types of equipment available for cost estimation.
| **Equipment** | **Equipment Type** |
|--------------------|--------------------------------------------|
| Blenders           | Kneader, Ribbon, Rotary                    |
| Centrifuges        | Auto batch separator, Centrifugal separator, Oscillating screen, Solid bowl w/o motor |
| Compressors        | Centrifugal, axial, and reciprocating, Rotary |
| Conveyors          | Apron, Belt, Pneumatic, Screw |
| Crystallizers      | Batch |
| Drives             | Gas turbine, Intern. comb. engine, Steam turbine, Electric—explosion-proof, Electric—totally enclosed, Electric—open/drip-proof |
| Dryers             | Drum, Rotary, gas fired, Tray |
| Dust Collectors    | Baghouse, Cyclone scrubbers, Electrostatic precipitator, Venturi scrubber |
| Evaporators        | Forced circulation (pumped), Falling film, Agitated film (scraped wall), Short tube, Long tube |
| Fans                | Centrifugal radial, Backward curve, Axial vane, Axial tube |
| Filters             | Bent, Cartridge, Disc and drum, Gravity, Leaf, Pan, Plate and frame, Table, Tube |
| Furnaces            | Reformer furnace, Pyrolysis furnace, Nonreactive fired heater |
| Heat exchangers     | Scraped wall, Teflon tube, Bayonet, Floating head, Fixed tube, U-tube, Kettle reboiler, Double pipe, Multiple pipe, Flat plate, Spiral plate, Air cooler, Spiral tube |
| Heaters             | Diphenyl heater, Molten salt heater, Hot water heater, Steam boiler |
| Mixers              | Impeller, Propeller, Turbine |
| Packing             | Loose (for towers) |
| Process vessels     | Horizontal, Vertical |
| Pumps               | Reciprocating, Positive displacement, Centrifugal |
| Reactors            | Autoclave, Fermenter, Inoculum tank, Jacketed agitated, Jacketed nonagitated, Mixer/settler |
| Screens             | DSM, Rotary, Stationary, Vibrating |
| Tanks               | API—fixed roof, API—floating roof |
| Towers              | Tray and packed |
| Trays               | Sieve, Valve, Demisters |
| Turbines            | Axial gas turbines, Radial gas/liquid expanders |
| Vaporizers          | Internal coils/jackets, Jacketed vessels |

## Modelling Description
### Bare Module
The bare module equipment cost ($C_{BM}$) represents the sum of direct and indirect cost and can be estimate by the following equation:

$C_{BM}=C_{p}^{o}\cdot F_{BM}$

Where: <br>
<span>&nbsp;&nbsp;&nbsp;&nbsp;</span>$C_{p}^{o}$: purchased cost for base conditions.<br>
<span>&nbsp;&nbsp;&nbsp;&nbsp;</span>$F_{BM}$: bare module cost factor.<br>

The $C_{p}^{o}$ represents the equipment cost made of the most commom material and operating at near-ambient pressures. Data for the purchased cost of the equipmentes were fitted to the following equation:

$log_{10}(C_{p}^{o})=K_{1} + K_{2}\cdot log_{10}(\Theta)+K_{3}\cdot log_{10}(\Theta)^{2}$

Where: <br>
<span>&nbsp;&nbsp;&nbsp;&nbsp;</span>$\Theta $: capacity or size parameter for the equipment.<br>
<span>&nbsp;&nbsp;&nbsp;&nbsp;</span>$K_{1}, K_{2}, K_{3}$: fitted parameters for the equipment<br>

> <span>**$${\color{red}Warning}$$**:</span> The values for the fitted parameters are valid only within a specific range of the size parameter.

The equation to calculate the bare module cost factor depends on the type of equipment, as show below:

| **Equipment**| **Sensibility**| **Equation** |
|--------------|----------------|--------------|
|**Blenders** <br> **Centrifuges** <br> **Conveyors** <br> **Crystallizers** <br> **Drives** <br> **Dryers** <br> **Dust Collectors** <br> **Filters** <br> **Mixers** <br> **Reactors** <br> **Screens** <br> | **• Pressure**: No  <br> **• Material**: No  <br> **• Type**: Yes | $F_{BM} = F_{BM}^o$
|**Compressors** <br> **Turbines** <br> **Packing** <br>|**• Pressure**: No  <br> **• Material**: Yes  <br> **• Type**: Yes| $F_{BM} = F_{BM}^{T,M}$|
|**Vaporizers** <br> **Evaporators** <br> **Fans** <br> |**• Pressure**: Yes  <br> **• Material**: Yes  <br> **• Type**: Yes| $F_{BM} = F_{BM}^{T,M}\cdot F_{P}$|
|**Heat Exchangers** <br> **Process Vessels** <br> **Tanks** <br> **Towers** <br> **Pumps** <br>|**• Pressure**: Yes  <br> **• Material**: Yes  <br> **• Type**: Yes| $F_{BM} = B_{1}+B_{2}\cdot F_{M}\cdot F_{P}$|
|**Furnances** <br> **Heaters** <br> |**• Pressure**: Yes  <br> **• Material**: Yes  <br> **• Type**: Yes| $F_{BM} = F_{BM}^{T,M}\cdot F_P\cdot F_T$|
|**Trays** <br> |**• Pressure**: No  <br> **• Material**: Yes  <br> **• Type**: Yes| $F_{BM} = F_{BM}^{T,M}\cdot N\cdot F_q$|


Where: <br>
<span>&nbsp;&nbsp;&nbsp;&nbsp;</span>$F_{BM}^o\ and \ F_{BM}^{T,M}$ : modulo cost factor value default and type/material dependent, respectively .<br>
<span>&nbsp;&nbsp;&nbsp;&nbsp;</span>$F_{P}$ : pressure factor.<br>
<span>&nbsp;&nbsp;&nbsp;&nbsp;</span>$F_{M}$ : material factor.<br>
<span>&nbsp;&nbsp;&nbsp;&nbsp;</span> $F_{T}$ : superheat correction factor for steam boilers. $F_{T}=1$ for heaters and furnance. $F_{T}=1+0.00184\cdot ΔT -0.00000335\cdot ΔT$, where $ΔT$ is the amountof superheat in °C.<br>
<span>&nbsp;&nbsp;&nbsp;&nbsp;</span>$N$: number of trays.<br>
<span>&nbsp;&nbsp;&nbsp;&nbsp; $F_{q}$: quantity factor. If $N≥20$, $F_{M}=1$ else $log_{10}(F_{M})=0.4771+0.08516\cdot log_{10}(N)-0.3473\cdot log_{10}(N)^2$.<br>

### Pressure Factor
The pressure factors, $F_P$, for the many process equipment is given by the following general form:

$log_{10}(F_p)=C_{1} + C_{2}\cdot log_{10}(P)+C_{3}\cdot log_{10}(P)^{2}$

Where: <br>
<span>&nbsp;&nbsp;&nbsp;&nbsp;</span>$P$ (barg): capacity or size parameter for the equipment.<br>
<span>&nbsp;&nbsp;&nbsp;&nbsp;</span>$C_{1}, C_{2}, C_{3}$: fitted parameters for the equipment.<br>

The pressure factor for horizontal and vertical process (pressurized) vessls of diameter $D$ meter and operating at pressure of $P$ barg is based in the ASME code for pressure vessel design.

$$
F_{P,\text{vessel}} = 
\begin{cases} 
1 & \text{for } t < t_{\text{min}} \text{ and } P > -0.5 \text{ barg} \\
(\frac{(P+1)\cdot D}{2 \cdot S \cdot E - 1.2 \cdot (P+1)}+CA)/t_{min} & \text{for } t > t_{\text{min}} \text{ and } P > -0.5 \text{ barg} \\
1.25 & \text{for } P < -0.5 \text{ barg}
\end{cases}
$$

Where: <br>
<span>&nbsp;&nbsp;&nbsp;&nbsp;</span>$t_{min}$ (m): capacity or size parameter for the equipment (default value = 0.0063).<br>
<span>&nbsp;&nbsp;&nbsp;&nbsp;</span>$S$ (bar): maximun allowable stress of material (default value = 944).<br>
<span>&nbsp;&nbsp;&nbsp;&nbsp;</span>$E$: weld efficiency (default value = 0.9).<br>
<span>&nbsp;&nbsp;&nbsp;&nbsp;</span>$CA$ (m): corrosion allowance (default value = 0.00315).<br>

### Inflation Effect on Equipment Cost 
When relying on past records or published correlations for price information, it is essential to be able to update these costs to account inflation effect. This correction is performed using the equation below:

$$
C_{p}^{o} = C_{po}^{o} \left( \frac{CEPCI}{CEPCI_o} \right)
$$

where: <br>
<span>&nbsp;&nbsp;&nbsp;&nbsp;</span>CEPCI: Chemical Engineering Plant Cost Index.

The subscripts "o" refers to the base time when cost is known (default value 397, referring to the year 2001).

