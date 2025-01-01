# New-Banh-Chung---Banh-Giay-Calculator-with-GUI

Author: Le Nhat Tan (42001078)  
Ton Duc Thang University

## Project Description
This program calculates the optimal number of Banh Chung (square sticky rice cake) and Banh Giay (round sticky rice cake) that can be made based on given ingredients and weather conditions. The project is based on the Vietnamese folk tale of Lang Lieu, who created these traditional cakes to honor both Heaven and Earth.

## Features
- Calculates optimal number of cakes based on available rice and leaves
- Handles different weather conditions that affect production:
  - Wind (optimizes for Banh Chung)
  - Rain (balances both types of cakes)
  - Sun (includes special calculations with bonus ingredients)
  - Fog (special case with minimal calculations)
  - Cloud (optimizes for Banh Giay with special conditions)
- Modern GUI interface for easy input and visualization
- Real-time results display
- Error handling and input validation

## Technical Requirements
- Python 3.x
- Required libraries:
  - tkinter (built-in)
  - math (built-in)

## Input Format
The program reads from `input.inp` with the following format:
```
n dc dg ld w
```
Where:
- n: Amount of sticky rice (integer ≤ 1000)
- dc: Side length of Banh Chung (positive integer)
- dg: Diameter of Banh Giay (positive integer)
- ld: Number of dong leaves (1-300)
- w: Weather condition (Rain/Sun/Cloud/Fog/Wind)

## Output Format
The program writes to `output.out` with the following format:
```
bc bg nd
```
Where:
- bc: Number of Banh Chung made
- bg: Number of Banh Giay made
- nd: Amount of remaining rice (rounded to 3 decimal places)

## Formulas Used
1. Rice needed for one Banh Chung: dc²
2. Rice needed for one Banh Giay: (dg² * π) / 4
where π = 3.1415926535

## Special Cases
1. **Wind Weather**: Prioritizes making Banh Chung
2. **Rain Weather**: Aims to balance both types of cakes
3. **Sun Weather**: Includes bonus rice calculations based on dimensions
4. **Fog Weather**: Returns initial dimensions and rice amount
5. **Cloud Weather**: 
   - If n and ld are amicable numbers: Returns all rice as remainder
   - Otherwise: Prioritizes making Banh Giay

## How to Run
1. Ensure Python is installed on your system
2. Create input.inp with appropriate values
3. Run the program:
```bash
python weather_calculator.py
```
4. Results will appear in the GUI and be saved to output.out

## Error Handling
- Returns "-1 -1 n" for invalid inputs:
  - n > 1000
  - ld < 1 or ld > 300
  - Invalid weather condition
  - Other invalid parameters

## Acknowledgments
- Based on the traditional Vietnamese folk tale of Lang Lieu
- Project requirements provided by Ton Duc Thang University
- Special thanks to Mr. Nguyen Quoc Thuan for project guidance
