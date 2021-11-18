# Load my functions.
library("tidyverse")
library("ggthemes")


theme_set(theme_few() + 
		  theme(plot.title=element_text(hjust=0.5)) 
)

setOpt <- function(height=5, width=6){
	options(repr.plot.height=height, 
			repr.plot.width=width)
}


getNameMap <- function(df, key, value){
	if (!is.data.frame(df)){
		stop("Input is not a dataframe.")
	}
	vec <- df[[value]] %>% setNames(df[[key]])
	return(vec)
}


plotDensity <- function(df, field, facet=NULL, nc=3, scl="free_x", bw=bw){
	input <- df %>%
			mutate(x=as.double(.[[field]]))
	if (is.null(facet)){
		input$facet <- "None"
	} else {
		input$facet <- df[[facet]]
	}
	statb <- input %>%
		group_by(facet) %>%
		summarise(n = n(), 
				  na_count = sum(is.na(x)), 
				  valid=sum(!is.na(x)),
				  v_max = max(x, na.rm=T) %>% round(1), 
				  v_min = min(x, na.rm=T) %>% round(1), 
				  v_mean = mean(x, na.rm=T) %>% round(1), 
				  .groups="drop"
				  ) 
	input <- input %>%
		filter(!is.na(x)) %>%
		left_join(statb, by="facet") %>%
		mutate(facet_label=str_c(facet, "\nTotal: ", n, ", NA: ", na_count, ", Valid: ", valid, 
								 ",\nMax: ", v_max, ", Min: ", v_min, ", Mean: ", v_mean))
	binw <- diff(range(input$x))/20
	facet_label <- getNameMap(input, "facet", "facet_label")
	p <- ggplot(input, aes(x=x)) + 
		geom_histogram(aes(y=..density..), binwidth=binw, fill="steelblue", color="white") + 
		geom_density(bw=bw) +
		labs(y="Density", x=field) + 
        scale_y_continuous(sec.axis = sec_axis(~.*binw*nrow(input), name="Count"), position="right")
	if (!is.null(facet)){
		p <- p + facet_wrap(~facet, ncol=nc, scale=scl, labeller = labeller(facet=facet_label))
	} else {
		p <- p + labs(title=str_c("Total: ", statb$n, ", NA: ", statb$na_count, ", Valid: ", statb$valid, 
								 ",\nMax: ", statb$v_max, ", Min: ", statb$v_min, ", Mean: ", statb$v_mean))

	}

	return(p)
}


