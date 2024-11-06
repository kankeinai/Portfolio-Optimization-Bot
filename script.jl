using JuMP
using Gurobi
using CSV
using DataFrames

function portfolio_optimization(path::String, M::Int,  budget::Union{Float64, Int}; analysis::Bool = false, advanced::Bool = false, 
    U::Union{Int, Nothing} = nothing, threshold::Union{Float64, Nothing, Int} = nothing, tolerance_level::Union{Float64, Nothing} = nothing, max_violation::Union{Float64, Nothing, Int} = nothing)
    
    redirect_stdout(devnull)
    df = CSV.read(path, DataFrame)

    projects = df[:, :project]
    profit =  df[:, :profit]
    costs = df[:, :cost]
    risks = df[:, :risk]

    N = length(projects)

    df[!, :dependence] = [
    try
        s === missing || isempty(s) ? nothing : Array(parse.(Int, split(strip(s, ['{', '}']), ",")))
    catch
        nothing  
    end
    for s in df.dependence
    ]
    U = isnothing(U) ? N : U
    random_matrix = rand(N, M)
    success_scenarios = random_matrix .> risks;

    model = Model(Gurobi.Optimizer)
    set_optimizer_attribute(model, "OutputFlag", 0)  # Turn off output

    @variable(model, x[1:N], Bin)
    @constraint(model, sum(x[i] for i=1:N) <= U)
    @objective(model, Max, sum(sum(profit[i] * x[i] * success_scenarios[i, j] for j in 1:M) / M for i in 1:N) - sum(costs[i] * x[i] for i in 1:N))
    @constraint(model, sum(costs[i]*x[i] for i in 1:N) <= budget)

    for k in 1:N
        if df[k, :dependence] ≠ nothing
            l = length(df[k, :dependence])
            if l>0 
                @constraint(model, sum(x[df[k, :dependence][i]] for i in 1:l) >= l * x[k])
            end
        end
    end

    if advanced
        @variable(model, u[1:M]<=0)
        @variable(model, v[1:M], Bin)
        @constraint(model, [j = 1:M], sum((profit[i]) * x[i] * success_scenarios[i, j] - costs[i]* x[i] for i in 1:N)>= threshold + u[j])
        @constraint(model, [j = 1:M], u[j] >= -v[j] * max_violation)
        @constraint(model, sum( v[j] for j in 1:M)/M <= 1 - tolerance_level)
    end


    optimize!(model)
    status = termination_status(model)

    if status == MOI.OPTIMAL || status == MOI.FEASIBLE_POINT || status == MOI.LOCALLY_SOLVED
    
        println("solution found.")

        if advanced
            prob = sum(value.(model[:v]))/M
        end

        stockh_x = value.(model[:x]);
        stockh_profit = objective_value(model);
        final_profits = (success_scenarios .* value.(model[:x]))' * profit 
        final_costs = sum(value.(model[:x]) .* costs)
    
        revenue = final_profits .- final_costs 
    
        if analysis
            perfect_information = zeros(N, M)
            for j in 1:M
    
                model = Model(Gurobi.Optimizer)
                set_optimizer_attribute(model, "OutputFlag", 0)
                @variable(model, x[1:N], Bin)
                @constraint(model, sum(x[i] for i=1:N) <= U)
                @objective(model, Max, sum(profit[i] * x[i] * success_scenarios[i, j] for i in 1:N) - sum(costs[i] * x[i] for i in 1:N))
                @constraint(model, sum(costs[i]*x[i] for i in 1:N) <= budget)
                for k in 1:N
                    if df[k, :dependence] ≠ nothing
                        l = length(df[k, :dependence])
                        if l>0 
                            @constraint(model, sum(x[df[k, :dependence][i]] for i in 1:l) >= l * x[k])
                        end
                    end
                end
                optimize!(model)
    
                perfect_information[:, j] = value.(model[:x])'
    
            end
            perfect_revenue = (success_scenarios.* perfect_information)' * profit - perfect_information' * costs;
            price_of_perfect_information = sum(perfect_revenue - revenue) * 1/M
    
            idx = rand(1:M)
            s = success_scenarios[:, idx];
    
            model = Model(Gurobi.Optimizer)
            set_optimizer_attribute(model, "OutputFlag", 0)
            @variable(model, x[1:N], Bin)
            @constraint(model, sum(x[i] for i=1:N) <= U)
            @objective(model, Max, sum(profit[i] * x[i] * s[i] for i in 1:N) - sum(costs[i] * x[i] for i in 1:N))
            @constraint(model, sum(costs[i]*x[i] for i in 1:N) <= budget)
            for k in 1:N
                if df[k, :dependence] ≠ nothing
                    l = length(df[k, :dependence])
                    if l>0 
                        @constraint(model, sum(x[df[k, :dependence][i]] for i in 1:l) >= l * x[k])
                    end
                end
            end
            optimize!(model)
            one_scenario = sum(sum(profit[i] * value.(model[:x])[i] * success_scenarios[i, j] for i in 1:N) for j in 1:M)/M - sum(costs[i] * value.(model[:x])[i] for i in 1:N)
            price_of_scenarios = stockh_profit - one_scenario 

            random_matrix_test = rand(N, M)
            success_scenarios_test = random_matrix_test .> risks;

            test_revenue = (success_scenarios_test .* stockh_x)' * profit .- sum(stockh_x .* costs);

            if advanced
                return (stockh_x, stockh_profit, revenue,  perfect_revenue, price_of_perfect_information,  price_of_scenarios, test_revenue, final_costs, prob)
            else
                return (stockh_x, stockh_profit, revenue,  perfect_revenue, price_of_perfect_information,  price_of_scenarios, test_revenue, final_costs)
            end
        else
            if advanced
                return (stockh_x, stockh_profit, revenue, prob)
            else
                return (stockh_x, stockh_profit, revenue)
            end
    
        end
    else
        println("No feasible solution found.")
        return nothing
    end
end

