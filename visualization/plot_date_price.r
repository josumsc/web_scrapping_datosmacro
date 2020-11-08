library(ggplot2)
library(dplyr)
library(tidyverse)
library(ggthemes)

dataset <- read.csv("data/oil_prices.csv")
dataset$yearmonth <- format(as.Date(dataset$date), "%Y-%m")

df <- dataset %>%
  select(yearmonth, opec, brent, wti) %>%
  gather(key = "type", value = "price", -yearmonth) %>%
  group_by(yearmonth, type) %>%
  summarize(mean_price = mean(price, na.rm = T))

ggplot(data = df, aes(x = yearmonth, y = mean_price)) +
  geom_line(aes(color = type, linetype = type, group = type)) +
  scale_colour_solarized('blue') +
  xlab('Year - Month') +
  ylab('Mean Price') +
  ggtitle('Mean Oil Price per Month (2000-2020)') +
  theme_solarized() +
  theme(axis.text.x = element_text(angle = 90, size=4), 
        plot.title = element_text(hjust = 0.5))
