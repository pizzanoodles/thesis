# FORECASTING
def get_insightinp(year, dict, inptype, inp):
    insight = '<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">\
    <div class="modal-dialog modal-dialog-scrollable modal-xl insightdiv">\
        <div class="modal-content">\
        <div class="modal-header">\
            <h5 class="modal-title" id="exampleModalLabel">Forecast Type: {inptype}</h5>\
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>\
        </div>\
        <div class="modal-body">\
                    <table class="table">\
                        <thead>\
                            <tr>\
                                <th scope="col">Year</th>\
                                <th scope="col">{inptype}</th>\
                            </tr>\
                        </thead>\
                        <tbody>'.format(inptype=inptype)
    for i in range(len(dict['Year'])):
        insight += '<tr>\
                <th scope="row">{year}</th>\
                <td>₱{amount:,.2f}</td>\
            </tr>'.format(year=dict["Year"][i], amount=dict[inptype][i])
    insight += '</tbody>\
                    </table></br></br>\
                    <div class="container-fluid">\
                        <h5>DATA</h5>\
                        <p>REVENUES</p>\
                            <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Corporis illum delectus nesciunt\
                            quidem! Asperiores minus quos nobis. Nihil, numquam ratione quae reiciendis molestias in\
                            dolor architecto sapiente. Vitae, provident quos.\
                            Nemo ullam illum repellat harum, voluptas ipsa temporibus! Sint eveniet maxime quisquam\
                            sunt. Ullam adipisci dolores fugit nam voluptatem ipsa, cumque fugiat rem ad corrupti\
                            voluptates blanditiis quidem cum repellat?\
                            Modi, ducimus ad? Quos, et harum hic beatae tempore, minima quibusdam autem, deserunt\
                            eveniet illo quod dolorum cumque doloribus! Corporis error a natus beatae placeat libero\
                            nulla ipsa minima aperiam?\
                            Ipsa sint, magnam vero dolorum obcaecati consequatur unde saepe minima voluptatibus\
                            consectetur, id aspernatur aliquam accusantium. Quas vitae officiis, ea obcaecati eligendi\
                            velit impedit sit. Ullam odit velit mollitia fuga.\
                            Vel dolorem, numquam excepturi cumque quidem debitis laudantium, quae deserunt sit expedita\
                            laborum ab? At ipsa aliquam maiores repellendus, est nostrum rem earum natus eaque laborum\
                            explicabo a soluta sapiente.Lorem, ipsum dolor sit amet consectetur adipisicing elit. Corporis illum delectus nesciunt\
                            quidem! Asperiores minus quos nobis. Nihil, numquam ratione quae reiciendis molestias in\
                            dolor architecto sapiente. Vitae, provident quos.\
                            Nemo ullam illum repellat harum, voluptas ipsa temporibus! Sint eveniet maxime quisquam\
                            sunt. Ullam adipisci dolores fugit nam voluptatem ipsa, cumque fugiat rem ad corrupti\
                            voluptates blanditiis quidem cum repellat?\
                            Modi, ducimus ad? Quos, et harum hic beatae tempore, minima quibusdam autem, deserunt\
                            eveniet illo quod dolorum cumque doloribus! Corporis error a natus beatae placeat libero\
                            nulla ipsa minima aperiam?\
                            Ipsa sint, magnam vero dolorum obcaecati consequatur unde saepe minima voluptatibus\
                            consectetur, id aspernatur aliquam accusantium. Quas vitae officiis, ea obcaecati eligendi\
                            velit impedit sit. Ullam odit velit mollitia fuga.\
                            Vel dolorem, numquam excepturi cumque quidem debitis laudantium, quae deserunt sit expedita\
                            laborum ab? At ipsa aliquam maiores repellendus, est nostrum rem earum natus eaque laborum\
                            explicabo a soluta sapiente.</p>\
                    </div>\
                </div>\
         </div >\
    < /div>\
    < /div>'
    return insight
