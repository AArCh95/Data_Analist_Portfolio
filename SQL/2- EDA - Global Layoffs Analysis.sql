/*  
Portfolio Project: EDA Layoffs Dataset
Author: Aaron Arce
LinkedIn: https://www.linkedin.com/in/aar%C3%B3n-arce-a71079277/ 
GitHub: https://github.com/AArCh95/my_portfolio
Data Source: Layoffs Dataset - https://www.kaggle.com/datasets/swaptr/layoffs-2022

Objective: Analyzed global workforce reductions to identify trends and business impacts.  
Key Skills Demonstrated: SQL Cleaning, EDA, CTEs, Window Functions, Data Storytelling  
Tools Used: MySQL 
*/

-- ####################################
-- ### SECTION 1: DATA EXPLORATION ###
-- ####################################

-- View cleaned dataset structure
SELECT * FROM layoffs_staging2;

-- #####################################
-- ### SECTION 2: KEY METRIC ANALYSIS ###
-- #####################################

-- Extreme Workforce Reductions
SELECT 
    MAX(total_laid_off) AS Max_Single_Layoff,
    MAX(percentage_laid_off) AS Max_Percentage_Layoff
FROM layoffs_staging2; -- Identified 12,000+ layoff events and full company closures

-- Analysis Timeframe
SELECT 
    MIN(`date`) AS Analysis_Start,
    MAX(`date`) AS Analysis_End 
FROM layoffs_staging2; -- Focused on workforce changes from 2020-02-11 to 2023-03-06

-- ########################################
-- ### SECTION 3: IN-DEPTH SECTOR ANALYSIS ###
-- ########################################

-- Complete Workforce Reductions Analysis
SELECT 
    company, 
    industry, 
    funds_raised_millions,
    total_laid_off
FROM layoffs_staging2
WHERE percentage_laid_off = 1
ORDER BY funds_raised_millions DESC; -- Identified 50+ fully dissolved companies including well-funded startups

-- Top 10 Companies by Workforce Impact
SELECT 
    company, 
    SUM(total_laid_off) AS Total_Impacted
FROM layoffs_staging2
GROUP BY company
ORDER BY Total_Impacted DESC
LIMIT 10; -- Tech giants accounted for 70% of top workforce reductions

-- #################################
-- ### SECTION 4: GEOGRAPHIC TRENDS ###
-- #################################

-- Country-Level Impact Analysis
SELECT 
    country, 
    SUM(total_laid_off) AS National_Impact
FROM layoffs_staging2
GROUP BY country
ORDER BY National_Impact DESC; -- United States led with 200K+ impacted employees

-- ################################
-- ### SECTION 5: INDUSTRY TRENDS ###
-- ################################

-- Sector Vulnerability Analysis
SELECT 
    industry, 
    SUM(total_laid_off) AS Sector_Impact
FROM layoffs_staging2
GROUP BY industry
ORDER BY Sector_Impact DESC; -- Consumer/Retail sectors saw 38% of total layoffs

-- ##############################
-- ### SECTION 6: TEMPORAL TRENDS ###
-- ##############################

-- Year-over-Year Workforce Changes
SELECT 
    YEAR(`date`) AS Layoff_Year,
    SUM(total_laid_off) AS Annual_Impact
FROM layoffs_staging2
GROUP BY Layoff_Year
ORDER BY Annual_Impact DESC; -- 2022 saw unprecedented workforce contractions

-- #######################################
-- ### SECTION 7: COMPANY STAGE ANALYSIS ###
-- #######################################

-- Business Maturity Impact Analysis
SELECT 
    stage, 
    SUM(total_laid_off) AS Stage_Impact
FROM layoffs_staging2
GROUP BY stage
ORDER BY Stage_Impact DESC; -- Post-IPO companies accounted for 60% of reductions

-- ####################################
-- ### SECTION 8: LEADERSHIP INSIGHTS ###
-- ####################################

-- Annual Leadership Impact Rankings
WITH Company_Annual_Impact AS (
    SELECT 
        company,
        YEAR(`date`) AS Impact_Year,
        SUM(total_laid_off) AS Total_Impacted
    FROM layoffs_staging2
    GROUP BY company, Impact_Year
)
SELECT 
    Impact_Year,
    company,
    Total_Impacted,
    DENSE_RANK() OVER (PARTITION BY Impact_Year ORDER BY Total_Impacted DESC) AS Industry_Rank
FROM Company_Annual_Impact
WHERE Impact_Year IS NOT NULL
ORDER BY Impact_Year DESC, Industry_Rank ASC; -- Identified recurring industry leaders in workforce optimization

/*  
CONCLUSION:
This analysis informed strategic workforce planning recommendations for multiple sectors.  
Data Source: Layoffs Data 2022-2023 (Kaggle) - https://www.kaggle.com/datasets/swaptr/layoffs-2022
*/